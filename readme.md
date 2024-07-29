# Gremlin Queries for Fraud Detection

The queries are designed to work with a graph schema that includes nodes with labels: `Entity`, `Intermediary`, `Address`, and `Officer`, and edges with labels: `intermediary_of`, `registered_address`, and `officer_of`. Node properties start with `n.` and edge properties start with `r.`.

## 1. Identify Entities with Many Intermediaries

Detect entities that are connected to many intermediaries, which might indicate complex structures.

```gremlin
g.V().hasLabel('Entity').as('e')
  .in('intermediary_of').as('i')
  .select('e', 'i')
  .by('n.name')
  .by('n.name')
  .groupCount().by(select('e'))
  .order(local).by(values, desc)
```

## 2. Identify Circular Relationships

Find cycles involving entities and intermediaries, which might indicate circular ownership or involvement.

```
g.V().hasLabel('Entity').as('e')
  .repeat(bothE().otherV().simplePath()).until(hasId('e'))
  .path()
```

## 3. Detect Entities Connected via Multiple Intermediaries

Identify entities that are connected through multiple intermediaries or officers.

```
g.V().hasLabel('Entity').as('e1')
  .repeat(bothE('intermediary_of', 'officer_of').otherV().simplePath()).times(2)
  .emit()
  .hasLabel('Entity').as('e2')
  .where('e1', neq('e2'))
  .select('e1', 'e2')
  .by('n.name')
```

## 4. Find Entities Registered at the Same Address

Identify entities registered at the same address, which might indicate attempts to hide relationships.

```
g.V().hasLabel('Address').as('a')
  .in('registered_address').as('e')
  .select('a', 'e')
  .by('n.address')
  .by('n.name')
  .groupCount().by(select('a'))
  .order(local).by(values, desc)
```

## 5. Find Entities with Multiple Addresses

Identify entities that are registered at multiple addresses, which might indicate an attempt to obscure their true location.

```gremlin
g.V().hasLabel('Entity').as('e')
  .out('registered_address').as('a')
  .select('e', 'a')
  .by('n.name')
  .by('n.address')
  .groupCount().by(select('e'))
  .order(local).by(values, desc)
```

## 6. Find Officers Associated with Multiple Entities

Detect officers who are associated with multiple entities. This might suggest involvement in multiple entities for potentially suspicious reasons.

```gremlin
g.V().hasLabel('Officer').as('o')
  .out('officer_of').as('e')
  .select('o', 'e')
  .by('n.name')
  .by('n.name')
  .groupCount().by(select('o'))
  .order(local).by(values, desc)
```

## 7. Detect Entities with Recent Changes

Identify entities that have had recent changes in their intermediary associations, which could indicate attempts to hide fraudulent activity.

```gremlin
g.V().hasLabel('Entity').as('e')
  .bothE('intermediary_of').has('r.start_date', gt('2024-01-01')) // Example recent date
  .otherV().as('i')
  .select('e', 'i')
  .by('n.name')
  .by('n.name')
  .groupCount().by(select('e'))
  .order(local).by(values, desc)
```

## 8. Find Entities with Unusual Address Patterns

Detect entities that are associated with addresses having unusual patterns or high frequency of registrations.

```gremlin
g.V().hasLabel('Address').as('a')
  .in('registered_address').as('e')
  .select('a', 'e')
  .by('n.address')
  .by('n.name')
  .groupCount().by(select('a'))
  .order(local).by(values, desc)
```


## 10. Detect Entities with Short-Term Intermediaries

Find entities that have had intermediaries for very short periods, which might indicate attempts to quickly change intermediaries to evade detection.

```gremlin
g.V().hasLabel('Entity').as('e')
  .bothE('intermediary_of').has('r.end_date', lt('2024-01-01')) // Example end date for short-term
  .has('r.start_date', gt('2023-01-01')) // Example start date for short-term
  .otherV().as('i')
  .select('e', 'i')
  .by('n.name')
  .by('n.name')
  .groupCount().by(select('e'))
  .order(local).by(values, desc)
```


## 10. Find Cycles in Graph

```gremlin
g.V().hasLabel('Entity')
  .repeat(.out().simplePath())
  .until(.loops().is(gte(1))
  .where(.in().hasLabel('Entity')))
  .path()
```
