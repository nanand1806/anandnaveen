# SBOM Pipeline (POC)

A proof-of-concept GitHub Actions workflow that generates, signs, and publishes a
Software Bill of Materials for this repository on every build.

## What it does

1. **Generate** - [Syft](https://github.com/anchore/syft) scans the repo and produces an
   SBOM in two standard formats (machine-readable JSON):
   - SPDX (`sbom.spdx.json`)
   - CycloneDX (`sbom.cdx.json`)
2. **Human-readable** - a small script converts the CycloneDX SBOM into an Excel workbook
   (`sbom.xlsx`) listing each component's name, version, type, PURL, and licenses.
3. **Sign** - [cosign](https://github.com/sigstore/cosign) signs each SBOM **keyless**
   (Sigstore OIDC), so no private keys or secrets are stored in the repo.
4. **Publish** - all SBOM artifacts (JSON, Excel, signatures, certificates) are uploaded
   as workflow artifacts.

## Triggers

- Manual (`workflow_dispatch`)
- Push to `main`
- Release published

## Run it

Actions tab -> **SBOM** -> *Run workflow*, then download the `sbom` artifact from the run.

## Verify a signature

```sh
cosign verify-blob \
  --certificate sbom.cdx.json.pem \
  --signature sbom.cdx.json.sig \
  --certificate-identity-regexp '.*' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  sbom.cdx.json
```
