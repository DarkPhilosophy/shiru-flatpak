#!/bin/bash
set -e

# Shiru Flatpak Build Script
# Usage: ./flatpak-build.sh [--repo REPO_PATH] [--clean] [--update] [--force-install] [--skip-install] [--system]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/flatpak-build.conf"

if [ -f "$CONFIG_FILE" ]; then
  # shellcheck source=/dev/null
  . "$CONFIG_FILE"
fi

REPO_PATH="${REPO_PATH:-${HOME}/.local/share/flatpak-shiru-repo}"
BUILD_DIR="${BUILD_DIR:-flatpak-build}"
MANIFEST="${MANIFEST:-.flatpak-manifest.yaml}"
CACHE_ROOT="${CACHE_ROOT:-${XDG_CACHE_HOME:-${HOME}/.cache}/shiru-flatpak}"
DOWNLOAD_DIR="${DOWNLOAD_DIR:-${CACHE_ROOT}/downloads}"
EXTRACT_CACHE_DIR="${EXTRACT_CACHE_DIR:-${CACHE_ROOT}/extracted}"
RELEASE_CACHE_DIR="${RELEASE_CACHE_DIR:-${CACHE_ROOT}/release}"
STAGING_DIR="${STAGING_DIR:-flatpak-staging}"
REMOTE_NAME="${REMOTE_NAME:-shiru-origin}"
APP_NAME="${APP_NAME:-Shiru}"
APP_ID="${APP_ID:-}"
GITHUB_REPO="${GITHUB_REPO:-RockinChaos/Shiru}"
DEB_ASSET_REGEX="${DEB_ASSET_REGEX:-\\.deb$}"
DEB_ARCH_REGEX="${DEB_ARCH_REGEX:-amd64|x86_64|linux}"
DEB_ASSET_FALLBACKS="${DEB_ASSET_FALLBACKS:-linux,amd64,x86_64}"
STRICT_ASSET="${STRICT_ASSET:-false}"

INSTALL_SCOPE="--user"
CLEAN=false
FORCE_UPDATE=false
FORCE_INSTALL=false
SKIP_INSTALL=false

if [ -z "$APP_ID" ]; then
  if command -v rg > /dev/null 2>&1; then
    APP_ID="$(rg -m1 '^app-id:' "$MANIFEST" | awk '{print $2}')"
  else
    APP_ID="$(grep -m1 '^app-id:' "$MANIFEST" | awk '{print $2}')"
  fi
fi

if [ -z "$APP_ID" ]; then
  echo "ERROR: Unable to read app-id from $MANIFEST"
  exit 1
fi

normalize_version() {
  printf '%s' "$1" | sed -E 's/^[^0-9]*//; s/[+].*$//'
}

version_lt() {
  local a b
  a="$(normalize_version "$1")"
  b="$(normalize_version "$2")"
  if [ -z "$a" ] || [ -z "$b" ]; then
    return 1
  fi
  if [ "$a" = "$b" ]; then
    return 1
  fi
  [ "$(printf '%s\n' "$a" "$b" | sort -V | head -n1)" = "$a" ]
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --repo)
      REPO_PATH="$2"
      shift 2
      ;;
    --clean)
      CLEAN=true
      shift
      ;;
    --update)
      FORCE_UPDATE=true
      shift
      ;;
    --force-install)
      FORCE_INSTALL=true
      shift
      ;;
    --skip-install)
      SKIP_INSTALL=true
      shift
      ;;
    --system)
      INSTALL_SCOPE="--system"
      shift
      ;;
    --check-upstream)
      CHECK_UPSTREAM=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--repo REPO_PATH] [--clean] [--update] [--force-install] [--skip-install] [--system] [--check-upstream]"
      exit 1
      ;;
  esac
done

if [ "$CHECK_UPSTREAM" = true ]; then
  echo "[0/5] Checking upstream version..."
  if [ -f ".scripts/check_upstream.py" ]; then
    # Run the python script and capture its exit code/behavior
    # We force the script to use a temporary output file if GITHUB_OUTPUT isn't set, 
    # to parse the decision locally.
    TEMP_OUTPUT="${GITHUB_OUTPUT:-.flatpak-build-output}"
    export GITHUB_OUTPUT="$TEMP_OUTPUT"
    
    python3 .scripts/check_upstream.py
    
    # Read variables from the output file
    if [ -f "$TEMP_OUTPUT" ]; then
      SHOULD_BUILD=$(grep "should_build=" "$TEMP_OUTPUT" | cut -d= -f2)
      TAG=$(grep "tag=" "$TEMP_OUTPUT" | cut -d= -f2)
      
      # Clean up if we created a temp file
      if [ "$TEMP_OUTPUT" = ".flatpak-build-output" ]; then
        rm "$TEMP_OUTPUT"
      fi
      
      if [ "$SHOULD_BUILD" = "false" ]; then
        echo "Upstream check indicates no update needed."
        exit 0
      fi
      
      echo "Update detected: $TAG"
      # Set FORCE_UPDATE to ensure we proceed with the build logic below
      FORCE_UPDATE=true
    fi
  else
    echo "WARNING: .scripts/check_upstream.py not found. Skipping check."
  fi
fi

echo "=========================================="
echo "${APP_NAME} Flatpak Build"
echo "=========================================="
echo "Repository: $REPO_PATH"
echo "Build dir:  $BUILD_DIR"
echo "Manifest:   $MANIFEST"
echo "App ID:     $APP_ID"
echo "Remote:     $REMOTE_NAME"
echo "Scope:      $INSTALL_SCOPE"
echo "=========================================="
echo ""

# Check dependencies
echo "[1/5] Checking dependencies..."
for cmd in flatpak flatpak-builder curl python3 ar tar; do
  if ! command -v "$cmd" &> /dev/null; then
    echo "ERROR: $cmd not found."
    exit 1
  fi
done
echo "✓ All dependencies found"

# Fetch latest release info and download .deb (cached)
echo ""
echo "[1.5/5] Checking latest release..."
case "$DOWNLOAD_DIR" in
  /*) ;;
  *) DOWNLOAD_DIR="${SCRIPT_DIR}/${DOWNLOAD_DIR}" ;;
esac
case "$EXTRACT_CACHE_DIR" in
  /*) ;;
  *) EXTRACT_CACHE_DIR="${SCRIPT_DIR}/${EXTRACT_CACHE_DIR}" ;;
esac
case "$RELEASE_CACHE_DIR" in
  /*) ;;
  *) RELEASE_CACHE_DIR="${SCRIPT_DIR}/${RELEASE_CACHE_DIR}" ;;
esac
case "$STAGING_DIR" in
  /*) ;;
  *) STAGING_DIR="${SCRIPT_DIR}/${STAGING_DIR}" ;;
esac

mkdir -p "$DOWNLOAD_DIR" "$EXTRACT_CACHE_DIR" "$RELEASE_CACHE_DIR"
mkdir -p "$CACHE_ROOT"

RELEASE_URL="https://api.github.com/repos/${GITHUB_REPO}/releases/latest"
RELEASE_JSON="${RELEASE_CACHE_DIR}/latest.json"
RELEASE_ETAG="${RELEASE_CACHE_DIR}/etag.txt"
HEADERS_TMP="$(mktemp)"
BODY_TMP="$(mktemp)"
ETAG_HEADER=""
if [ -f "$RELEASE_ETAG" ]; then
  ETAG_HEADER="$(cat "$RELEASE_ETAG")"
fi

HTTP_CODE="$(curl -sS -D "$HEADERS_TMP" -o "$BODY_TMP" -H "If-None-Match: ${ETAG_HEADER}" "$RELEASE_URL" -w "%{http_code}")"

case "$HTTP_CODE" in
  200)
    mv "$BODY_TMP" "$RELEASE_JSON"
    awk 'BEGIN{IGNORECASE=1} /^etag:/ {print $2}' "$HEADERS_TMP" | tr -d '\r' > "$RELEASE_ETAG"
    ;;
  304)
    if [ -f "$RELEASE_JSON" ]; then
      rm -f "$BODY_TMP"
    else
      echo "ERROR: Received 304 but no cached release data."
      rm -f "$BODY_TMP"
      exit 1
    fi
    ;;
  403|429)
    if [ -f "$RELEASE_JSON" ]; then
      echo "WARNING: GitHub API rate-limited; using cached release data."
      rm -f "$BODY_TMP"
    else
      echo "ERROR: GitHub API rate-limited and no cached release data."
      rm -f "$BODY_TMP"
      exit 1
    fi
    ;;
  *)
    if [ -f "$RELEASE_JSON" ]; then
      echo "WARNING: GitHub API error (${HTTP_CODE}); using cached release data."
      rm -f "$BODY_TMP"
    else
      echo "ERROR: Unable to fetch release data (HTTP ${HTTP_CODE})."
      rm -f "$BODY_TMP"
      exit 1
    fi
    ;;
esac
rm -f "$HEADERS_TMP"

RELEASE_INFO="$(cat "$RELEASE_JSON" | python3 .scripts/resolve_asset.py "$DEB_ASSET_REGEX" "$DEB_ARCH_REGEX" "$DEB_ASSET_FALLBACKS")"

if [ -z "$RELEASE_INFO" ]; then
  if [ "$STRICT_ASSET" = "true" ]; then
    echo "ERROR: Unable to resolve latest release for $GITHUB_REPO"
    exit 1
  fi
  echo "WARNING: No matching .deb asset found; skipping."
  exit 0
fi

RELEASE_TAG="$(printf '%s' "$RELEASE_INFO" | awk -F'|' '{print $1}')"
ASSET_NAME="$(printf '%s' "$RELEASE_INFO" | awk -F'|' '{print $2}')"
ASSET_URL="$(printf '%s' "$RELEASE_INFO" | awk -F'|' '{print $3}')"
METADATA_VERSION="$(normalize_version "$RELEASE_TAG")"
if [ -z "$METADATA_VERSION" ]; then
  echo "WARNING: Unable to normalize version from tag ${RELEASE_TAG}"
fi

LAST_BUILT_FILE="${CACHE_ROOT}/last-built-version.txt"
DEB_FILE="${DOWNLOAD_DIR}/${ASSET_NAME}"

if command -v rg > /dev/null 2>&1; then
  RUNTIME="$(rg -m1 '^runtime:' "$MANIFEST" | awk '{print $2}')"
  RUNTIME_VERSION="$(rg -m1 '^runtime-version:' "$MANIFEST" | awk '{print $2}')"
  SDK="$(rg -m1 '^sdk:' "$MANIFEST" | awk '{print $2}')"
else
  RUNTIME="$(grep -m1 '^runtime:' "$MANIFEST" | awk '{print $2}')"
  RUNTIME_VERSION="$(grep -m1 '^runtime-version:' "$MANIFEST" | awk '{print $2}')"
  SDK="$(grep -m1 '^sdk:' "$MANIFEST" | awk '{print $2}')"
fi

RUNTIME_VERSION="$(printf '%s' "$RUNTIME_VERSION" | tr -d "'\"")"
ARCH="$(flatpak --default-arch 2>/dev/null || echo x86_64)"
RUNTIME_ID="${RUNTIME}/${ARCH}/${RUNTIME_VERSION}"
SDK_ID="${SDK}/${ARCH}/${RUNTIME_VERSION}"

if [ -z "$RUNTIME" ] || [ -z "$RUNTIME_VERSION" ] || [ -z "$SDK" ]; then
  echo "ERROR: Unable to read runtime/sdk info from $MANIFEST"
  exit 1
fi

LAST_BUILT=""
if [ -f "$LAST_BUILT_FILE" ]; then
  LAST_BUILT="$(cat "$LAST_BUILT_FILE")"
fi

INFO_USER="$(flatpak info --user --show-metadata "$APP_ID" 2>/dev/null || true)"
INFO_SYSTEM="$(flatpak info --system --show-metadata "$APP_ID" 2>/dev/null || true)"
INFO_OUTPUT=""
INSTALLED=false
INSTALLED_VERSION=""
INSTALLED_RUNTIME=""
INSTALLED_SCOPE="none"

if [ -n "$INFO_USER" ]; then
  INFO_OUTPUT="$INFO_USER"
  INSTALLED_SCOPE="user"
fi

if [ -n "$INFO_SYSTEM" ]; then
  if [ "$INSTALLED_SCOPE" = "user" ]; then
    INSTALLED_SCOPE="both"
  else
    INFO_OUTPUT="$INFO_SYSTEM"
    INSTALLED_SCOPE="system"
  fi
fi

if [ -n "$INFO_OUTPUT" ]; then
  INSTALLED=true
  INSTALLED_VERSION="$(printf '%s\n' "$INFO_OUTPUT" | awk -F= '$1=="version" {print $2; exit}')"
  INSTALLED_RUNTIME="$(printf '%s\n' "$INFO_OUTPUT" | awk -F= '$1=="runtime" {print $2; exit}')"
fi

EXTRACT_VERSION_DIR="${EXTRACT_CACHE_DIR}/${RELEASE_TAG}"
HAS_EXTRACT=false
if [ -d "$EXTRACT_VERSION_DIR" ]; then
  HAS_EXTRACT=true
fi

echo "Latest release: ${RELEASE_TAG}"
echo "Meta version:   ${METADATA_VERSION}"
if [ -n "$INSTALLED_VERSION" ]; then
  echo "Installed ver:  ${INSTALLED_VERSION}"
else
  echo "Installed ver:  (unknown)"
fi
if [ -n "$INSTALLED_RUNTIME" ]; then
  echo "Installed rt:   ${INSTALLED_RUNTIME}"
fi
if [ "$INSTALLED_SCOPE" = "system" ] && [ "$INSTALL_SCOPE" = "--user" ]; then
  echo "NOTE: System install detected; user install will not update system metadata."
  echo "      Use: flatpak info --user ${APP_ID}"
fi
echo "Cached extract: ${HAS_EXTRACT}"
if [ -n "$LAST_BUILT" ]; then
  echo "Last built:     ${LAST_BUILT}"
fi

NEED_UPDATE=false
if [ -z "$METADATA_VERSION" ]; then
  NEED_UPDATE=true
elif [ "$INSTALLED" = false ]; then
  NEED_UPDATE=true
elif [ -z "$INSTALLED_VERSION" ]; then
  NEED_UPDATE=true
elif version_lt "$INSTALLED_VERSION" "$RELEASE_TAG"; then
  NEED_UPDATE=true
fi

RUNTIME_CHANGED=false
if [ "$INSTALLED" = true ] && [ -n "$INSTALLED_RUNTIME" ] && [ "$INSTALLED_RUNTIME" != "$RUNTIME_ID" ]; then
  RUNTIME_CHANGED=true
  FORCE_INSTALL=true
  echo "WARNING: Installed runtime ${INSTALLED_RUNTIME} != target ${RUNTIME_ID}; forcing reinstall."
fi

if [ "$FORCE_INSTALL" = true ] && [ "$INSTALLED" = true ] && [ "$INSTALLED_VERSION" = "$RELEASE_TAG" ]; then
  echo "WARNING: Forcing reinstall of ${APP_ID} at ${RELEASE_TAG}"
fi

if [ "$INSTALLED" = true ] && [ "$INSTALLED_VERSION" != "" ] && version_lt "$RELEASE_TAG" "$INSTALLED_VERSION"; then
  echo "WARNING: Installed version ${INSTALLED_VERSION} is newer than ${RELEASE_TAG}"
fi

if [ "$FORCE_INSTALL" = false ] && [ "$FORCE_UPDATE" = false ] && [ "$NEED_UPDATE" = false ] && [ "$INSTALLED" = true ] && [ "$RUNTIME_CHANGED" = false ]; then
  echo "Installed version is current; skipping build and install."
  exit 0
fi

NEED_DOWNLOAD=true
if [ "$HAS_EXTRACT" = true ] && [ "$FORCE_UPDATE" = false ]; then
  NEED_DOWNLOAD=false
fi

if [ "$NEED_DOWNLOAD" = true ]; then
  echo "Downloading ${ASSET_NAME} (${RELEASE_TAG})..."
  curl -fL "$ASSET_URL" -o "${DEB_FILE}.tmp"
  mv "${DEB_FILE}.tmp" "$DEB_FILE"
else
  echo "Using cached extract for ${RELEASE_TAG}"
fi

# Extract .deb to a versioned cache directory and stage for build
CURRENT_EXTRACT_DIR="${STAGING_DIR}/current"

if [ "$FORCE_UPDATE" = true ] && [ -d "$EXTRACT_VERSION_DIR" ]; then
  rm -rf "$EXTRACT_VERSION_DIR"
fi

if [ ! -d "$EXTRACT_VERSION_DIR" ]; then
  echo "Extracting ${ASSET_NAME}..."
  WORK_DIR="$(mktemp -d "${DOWNLOAD_DIR}/extract-XXXXXX")"
  (
    cd "$WORK_DIR"
    ar x "$DEB_FILE"
  )
  DATA_TAR="$(find "$WORK_DIR" -maxdepth 1 -type f -name 'data.tar.*' | head -n1)"
  if [ -z "$DATA_TAR" ]; then
    echo "ERROR: data.tar.* not found in $WORK_DIR"
    exit 1
  fi
  mkdir -p "$EXTRACT_VERSION_DIR"
  tar -xf "$DATA_TAR" -C "$EXTRACT_VERSION_DIR"
  rm -rf "$WORK_DIR"
  rm -f "$DEB_FILE"
fi

rm -rf "$STAGING_DIR"
mkdir -p "$CURRENT_EXTRACT_DIR"
if ! cp -al "$EXTRACT_VERSION_DIR"/. "$CURRENT_EXTRACT_DIR"/ >/dev/null 2>&1; then
  cp -a "$EXTRACT_VERSION_DIR"/. "$CURRENT_EXTRACT_DIR"/
fi

# Clean if requested
if [ "$CLEAN" = true ]; then
  echo ""
  echo "[2/5] Cleaning previous build..."
  rm -rf "$BUILD_DIR"
  mkdir -p "$BUILD_DIR"
  echo "✓ Build directory cleaned"
else
  echo ""
  echo "[2/5] Preparing build directory..."
  mkdir -p "$BUILD_DIR"
  echo "✓ Build directory ready"
fi

# Generate manifest with version metadata for installed version reporting
MANIFEST_FOR_BUILD="${SCRIPT_DIR}/.flatpak-manifest.generated.yaml"
METADATA_FILE="${SCRIPT_DIR}/.flatpak-metadata.ini"
python3 .scripts/generate_manifest.py "$MANIFEST" "$MANIFEST_FOR_BUILD" "$METADATA_FILE"

cat > "$METADATA_FILE" << EOF
[Application]
name=${APP_ID}
runtime=${RUNTIME_ID}
sdk=${SDK_ID}
version=${METADATA_VERSION}
EOF

# Create repository if needed
echo ""
echo "[3/5] Setting up Flatpak repository..."
mkdir -p "$REPO_PATH"
REPO_PATH="$(cd "$REPO_PATH" && pwd)"
REMOTE_URL="file://$REPO_PATH"
echo "✓ Repository ready at $REPO_PATH ($INSTALL_SCOPE)"

# Build the Flatpak
echo ""
echo "[4/5] Building Flatpak package..."
flatpak-builder \
  --repo="$REPO_PATH" \
  --force-clean \
  --disable-rofiles-fuse \
  "$BUILD_DIR" \
  "$MANIFEST_FOR_BUILD"

BUILD_RESULT=$?
if [ $BUILD_RESULT -eq 0 ]; then
  echo "✓ Flatpak build completed successfully"
  echo "$RELEASE_TAG" > "$LAST_BUILT_FILE"
  flatpak build-update-repo "$REPO_PATH"
  rm -rf "$STAGING_DIR"
  if [ -d "$EXTRACT_CACHE_DIR" ]; then
    find "$EXTRACT_CACHE_DIR" -mindepth 1 -maxdepth 1 -type d ! -name "$RELEASE_TAG" -exec rm -rf {} +
  fi
  if [ -d "$DOWNLOAD_DIR" ]; then
    find "$DOWNLOAD_DIR" -maxdepth 1 -type f -name '*.deb' -exec rm -f {} +
  fi
else
  echo "✗ Flatpak build failed with exit code $BUILD_RESULT"
  exit $BUILD_RESULT
fi

# Install the built Flatpak
if [ "$SKIP_INSTALL" = true ]; then
  echo ""
  echo "[5/5] Skipping install (--skip-install)"
  echo ""
  echo "=========================================="
  echo "✓ Build complete (install skipped)"
  echo "=========================================="
  echo ""
  exit 0
fi

CURRENT_URL="$(flatpak remotes $INSTALL_SCOPE --show-details 2>/dev/null | awk -v name="$REMOTE_NAME" '$1==name {print $3; exit}')"
if [ -z "$CURRENT_URL" ]; then
  flatpak remote-add $INSTALL_SCOPE --no-gpg-verify "$REMOTE_NAME" "$REMOTE_URL"
else
  if [ "$CURRENT_URL" != "$REMOTE_URL" ]; then
    flatpak remote-modify $INSTALL_SCOPE --url="$REMOTE_URL" "$REMOTE_NAME"
  fi
  flatpak remote-modify $INSTALL_SCOPE --no-gpg-verify "$REMOTE_NAME"
fi

echo ""
echo "[5/5] Installing Flatpak..."
INSTALL_ARGS="-y"
if [ "$FORCE_INSTALL" = true ]; then
  INSTALL_ARGS="$INSTALL_ARGS --reinstall"
fi
flatpak install $INSTALL_ARGS $INSTALL_SCOPE "$REMOTE_NAME" "$APP_ID"

echo ""
echo "=========================================="
echo "✓ Build and installation complete!"
echo "=========================================="
echo ""
echo "To run ${APP_NAME}:"
echo "  flatpak run ${APP_ID}"
echo ""
echo "To add to applications menu:"
echo "  flatpak run ${APP_ID} &"
echo ""
echo "To uninstall:"
echo "  flatpak uninstall ${APP_ID}"
echo ""
