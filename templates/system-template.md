# [System Component Name]

**Purpose**: [What this system doc describes]
**Updated**: [Date]

---

## Overview

[High-level description of this system component, architecture, or pattern]

**Why this exists**:
- [Reason 1]
- [Reason 2]
- [Reason 3]

---

## Architecture

### High-Level Design

```
[ASCII diagram or description of architecture]

Component A ──> Component B ──> Component C
     │              │               │
     └──────────────┴───────────────┘
              Central Store
```

### Components

#### Component 1: [Name]
**Responsibility**: [What it does]
**Location**: `src/path/to/component`
**Key Files**:
- `file1.ts` - [Purpose]
- `file2.ts` - [Purpose]

#### Component 2: [Name]
**Responsibility**: [What it does]
**Location**: `src/path/to/component`
**Key Files**:
- `file1.ts` - [Purpose]
- `file2.ts` - [Purpose]

---

## Patterns & Conventions

### Pattern 1: [Name]

**When to use**:
- [Scenario 1]
- [Scenario 2]

**How it works**:
```typescript
// Code example showing pattern
interface Example {
  property: string;
}

function usePattern(): Example {
  // Implementation
  return { property: 'value' };
}
```

**Benefits**:
- [Benefit 1]
- [Benefit 2]

**Common mistakes to avoid**:
- ❌ [Mistake 1]
- ❌ [Mistake 2]
- ✅ [Correct approach]

### Pattern 2: [Name]

[Similar structure as Pattern 1]

---

## Data Flow

### Flow 1: [Scenario Name]

```
1. User action
   ↓
2. Event handler
   ↓
3. Business logic
   ↓
4. State update
   ↓
5. UI render
```

**Example**:
```typescript
// Complete code example showing this flow
async function handleAction() {
  // 1. Trigger
  const input = getUserInput();

  // 2. Process
  const result = await processData(input);

  // 3. Update
  updateState(result);
}
```

---

## Configuration

### Required Settings

```typescript
// Configuration interface
interface Config {
  option1: string;  // Description
  option2: number;  // Description
  option3: boolean; // Description
}
```

### Environment Variables

```bash
# .env.example
VARIABLE_NAME=value  # Description of what this does
ANOTHER_VAR=value    # Description
```

### Default Values

```typescript
const defaults: Config = {
  option1: 'default',
  option2: 100,
  option3: true,
};
```

---

## API / Interface

### Public Methods

#### `functionName(param: Type): ReturnType`

**Purpose**: [What this function does]

**Parameters**:
- `param` (Type): [Description]

**Returns**: [Description]

**Example**:
```typescript
const result = functionName('example');
```

**Throws**:
- `ErrorType`: [When this error occurs]

#### `anotherFunction()`

[Similar structure for each public method]

---

## Performance Considerations

### Optimization 1: [Name]
**Problem**: [What was slow]
**Solution**: [How it's optimized]
**Impact**: [Measured improvement]

### Optimization 2: [Name]
**Problem**: [What was slow]
**Solution**: [How it's optimized]
**Impact**: [Measured improvement]

### Best Practices
- ✅ [Practice 1]
- ✅ [Practice 2]
- ❌ Avoid [Anti-pattern 1]
- ❌ Avoid [Anti-pattern 2]

---

## Testing

### Unit Tests
**Location**: `tests/unit/`

**What's covered**:
- [ ] [Test scenario 1]
- [ ] [Test scenario 2]
- [ ] [Test scenario 3]

**Example test**:
```typescript
describe('Component', () => {
  it('should do something', () => {
    // Test implementation
    expect(result).toBe(expected);
  });
});
```

### Integration Tests
**Location**: `tests/integration/`

**What's covered**:
- [ ] [Integration scenario 1]
- [ ] [Integration scenario 2]

---

## Common Issues & Solutions

### Issue 1: [Problem Description]
**Symptoms**: [What you see]
**Cause**: [Why it happens]
**Solution**: [How to fix]

**Related SOP**: [Link to sops/debugging/issue.md]

### Issue 2: [Problem Description]
[Similar structure]

---

## Examples

### Example 1: Basic Usage

```typescript
// Complete, working example
import { Component } from './component';

function example() {
  const component = new Component({
    config: 'value'
  });

  return component.execute();
}
```

### Example 2: Advanced Usage

```typescript
// More complex example
import { Component, Helper } from './component';

async function advancedExample() {
  const helper = new Helper();
  const component = new Component({
    helper,
    advanced: true
  });

  const result = await component.executeAsync();
  return helper.transform(result);
}
```

---

## Dependencies

### Internal Dependencies
- `src/path/to/module` - [Why needed]
- `src/another/module` - [Why needed]

### External Dependencies
- `package-name` - [Version] - [Why needed]
- `another-package` - [Version] - [Why needed]

---

## Migration Guide

### From Previous Version

**Breaking Changes**:
1. [Change 1]: [How to update]
2. [Change 2]: [How to update]

**Example migration**:
```typescript
// Before
oldAPI.method();

// After
newAPI.method({ config: 'value' });
```

---

## Future Enhancements

### Planned Improvements
- [ ] [Enhancement 1] - [Reason]
- [ ] [Enhancement 2] - [Reason]

### Under Consideration
- [ ] [Idea 1] - [Potential benefit]
- [ ] [Idea 2] - [Potential benefit]

---

## Related Documentation

**System Docs**:
- [system/related-system.md](./related-system.md)

**SOPs**:
- [sops/integrations/related.md](../sops/integrations/related.md)

**External Resources**:
- [Official Documentation](https://example.com)
- [Tutorial](https://example.com/tutorial)

---

## Change Log

### [Date] - Major Update
- [Change 1]
- [Change 2]

### [Date] - Initial Creation
- Created by [Name]
- Initial architecture design

---

**Maintained By**: [Team/Person]
**Last Reviewed**: [Date]
