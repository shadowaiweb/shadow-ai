# SHADOW source bundle

The full SHADOW 3.0 Stage 12 source is stored in `.shadow/source_bundle.zip` for the GitHub build workflow. This avoids the GitHub web uploader's 100-file limit.

The workflow extracts the bundle into `build_src/`, runs the release checks and tests there, builds `SHADOW.exe`, runs the packaged diagnostics check, then creates the portable Windows ZIP and installer artifacts.

The design-reference PNG was intentionally omitted from the CI bundle because the runtime does not depend on it.
