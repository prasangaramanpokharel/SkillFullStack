# Relational Normalization & Dependency Theory Reference

Comprehensive mathematical and practical guide to relational normalization (1NF through BCNF and 5NF).

---

## 1. Functional Dependencies & Keys

- **Functional Dependency ($X \rightarrow Y$)**:
  Given relation $R$, attribute set $Y$ is functionally dependent on $X$ if each $X$-value in $R$ is associated with precisely one $Y$-value.
- **Candidate Key**:
  A minimal superkey: a set of attributes that uniquely determines all other attributes in the relation, with no proper subset that does the same.
- **Prime Attribute**: An attribute that is a member of any candidate key.
- **Determinant**: Any attribute or set of attributes upon which some other attribute is functionally dependent.

---

## 2. Normal Forms Hierarchy

```
       [ 1NF ]  Atomic attributes & unique tuples
          |
       [ 2NF ]  No partial dependencies on candidate keys
          |
       [ 3NF ]  No transitive dependencies on candidate keys
          |
       [ BCNF ] Every determinant is a candidate key
          |
       [ 4NF ]  No multi-valued dependencies (MVD)
          |
       [ 5NF ]  No join dependencies (PJNF)
```

### First Normal Form (1NF)
- Each attribute must contain atomic (indivisible) values.
- No repeating groups or arrays stored as comma-separated text.
- Must have an identifiable primary key.

### Second Normal Form (2NF)
- Relation is in 1NF.
- No non-prime attribute is partially dependent on any candidate key.
- (Applies when candidate keys are composite. If all candidate keys are single attributes, 1NF implies 2NF).

### Third Normal Form (3NF)
- Relation is in 2NF.
- No transitive dependencies: if $X \rightarrow Y$ and $Y \rightarrow Z$, then non-prime attribute $Z$ must not depend on $X$ through non-prime $Y$.
- Formal rule: For every non-trivial $X \rightarrow Y$, either $X$ is a superkey OR $Y$ is a prime attribute.

### Boyce-Codd Normal Form (BCNF)
- Stricter than 3NF: For EVERY non-trivial functional dependency $X \rightarrow Y$, $X$ MUST be a superkey.
- Eliminates anomalies when candidate keys overlap composite attributes.

---

## 3. Lossless Decomposition & Dependency Preservation

When decomposing relation $R$ into $R_1$ and $R_2$:
1. **Lossless Join**:
   $R_1 \bowtie R_2 = R$ if and only if $R_1 \cap R_2 \rightarrow R_1$ OR $R_1 \cap R_2 \rightarrow R_2$.
2. **Dependency Preservation**:
   All original functional dependencies can be enforced using the local constraints of decomposed relations without performing expensive joins.
