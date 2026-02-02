# Source References

## Official Repositories

- **Python**: https://github.com/approvals/ApprovalTests.Python
- **Java**: https://github.com/approvals/ApprovalTests.Java
- **Node.js**: https://github.com/approvals/Approvals.NodeJS

## Key Source Files

### Python
- `approvaltests/approvals.py` - Core verify functions
- `approvaltests/scrubbers/` - Scrubber implementations
- `approvaltests/namer/namer_factory.py` - NamerFactory for parametrized tests
- `approvaltests/utilities/simple_logger.py` - SimpleLogger for log verification

### Java
- `approvaltests/src/main/java/org/approvaltests/Approvals.java` - Core API
- `approvaltests/src/main/java/org/approvaltests/scrubbers/DateScrubber.java` - Date scrubbing
- `approvaltests/src/main/java/org/approvaltests/namer/NamerFactory.java` - Multiple approvals
- `approvaltests/src/main/java/org/approvaltests/utils/ConsoleOutput.java` - Console capture

### Node.js
- `lib/Providers/Jest/JestApprovals.ts` - Jest integration
- `lib/Scrubbers/Scrubbers.ts` - Scrubber utilities
- `lib/Scrubbers/DateScrubber.ts` - Date scrubbing
- `lib/Core/Options.ts` - Options class

## Important Patterns

### Scrubbers
- GUIDs → `guid_1`, `guid_2` (consistent replacement)
- Dates → `[Date1]`, `[Date2]` (auto-detect format from example)
- Regex → custom pattern with static or indexed replacement
- Combining → chain multiple scrubbers

### Multiple Approvals Per Test
- Python: `NamerFactory.with_parameters()`
- Java: `NamerFactory.withParameters()`, `NamerFactory.useMultipleFiles()`
- Node.js: Not supported

### Inline Approvals
- Python: Docstrings with `verify()` options
- Java: Text blocks (`"""`) with `Options().inline(expected)`
- Node.js: Not supported (use Jest's `toMatchInlineSnapshot()` instead)

## Feature Availability

### All Languages
- verify, verifyAsJson, verifyAll
- Scrubbers (GUID, date, regex, custom)
- Options (scrubber, reporter, file extension)
- Combination testing

### Python + Java Only
- Multiple approvals per test (NamerFactory)
- Inline approvals
- Console/log output capture

### Java Only
- `@UseReporter` annotation
- PackageSettings configuration
- OS/machine-specific test naming
