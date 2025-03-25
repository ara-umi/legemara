env_export:
    conda env export --no-builds | grep -v '^prefix:' > environment.yaml

.PHONY: env_export
