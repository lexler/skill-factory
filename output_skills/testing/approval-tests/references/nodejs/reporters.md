# Node.js Reporters

Reporters handle what happens when an approval fails.

## Contents

- [Available Reporters](#available-reporters)
- [MultiReporter](#multireporter)
- [Custom Reporter](#custom-reporter)

## Available Reporters

Pass as strings to `reporters` config:

**Diff tools:** BeyondCompare, diffmerge, p4merge, tortoisemerge, meld, kdiff3, vimdiff

**Editors:** vscode, vscodium, visualstudio

**Console:** nodediff, gitdiff

**CI-friendly:** copycommand (outputs copy command), donothing (silent fail)

```javascript
approvals.configure({
  reporters: ['BeyondCompare', 'vscode', 'gitdiff']
});
```

## MultiReporter

Try reporters in order until one works:

```javascript
const { MultiReporter } = approvals.reporters;

approvals.configure({
  reporters: [new MultiReporter(['p4merge', 'vscode', 'copycommand'])]
});
```

## Custom Reporter

```javascript
approvals.configure({
  reporters: [{
    name: 'my-reporter',
    canReportOn: (filePath) => true,
    report: (approvedPath, receivedPath) => {
      console.log(`Diff: ${approvedPath} vs ${receivedPath}`);
    }
  }]
});
```

Interface:
- `name` - Reporter identifier
- `canReportOn(filePath)` - Return true if reporter can handle this file
- `report(approvedPath, receivedPath)` - Handle the mismatch
