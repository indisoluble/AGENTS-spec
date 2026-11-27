# Maintaining the evaluation engine

Start with the engine requirement and the runtime component that implements it. Use ordinary functions, the existing typed result records, paths for filesystem boundaries and bytes for exact content. Two callers alone do not justify a generic utility. Keep scenario policy with the caller.

Supply execution substitutes through the documented interfaces. Distinguish an absent observation from an observed empty state, and an infrastructure error from a false assertion. For snapshot changes, exercise comparison and missing-byte controls before verifying the consuming case. Preserve independent negative controls, including cleanup and evidence failures.

See [engine interfaces](framework-design.md#interfaces-used-by-scenarios-and-substitutes) and [engine verification](../README.md).
