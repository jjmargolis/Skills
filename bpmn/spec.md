# BPMN 2.0.2, distilled

Source: OMG *Business Process Model and Notation*, v2.0.2, formal/2013-12-09 (`formal-13-12-09.PDF`, 532 pages). Every statement below comes from that PDF, all 532 pages of which were read for this file; nothing is from memory. `(§x, p.n)` = spec clause and printed page. `(fig)` = taken from a figure because the text does not say it. Where the spec contradicts itself, both readings are in §14 and flagged `[!]` inline.

Notation here: `attr: Type [mult] = default`. MUST/MAY carry their RFC 2119 meaning, as in the spec. SF = Sequence Flow, MF = Message Flow.

---

## 1. What BPMN is (§1, §7; pp.1, 19–46)

- A notation, a metamodel and an interchange format for business processes. Uses XML Schema for data types, XPath for expressions, WSDL for services (replaceable).
- Out of scope: organisation models and resources, functional breakdowns, data and information models, strategy, business rules, simulation, monitoring, deployment. It shows data moving but is not a data-flow language.
- Three sub-models:
  - **Process** (orchestration): one participant's flow. *Private* (internal; executable or non-executable) or *public* (only the activities that talk to other participants, and their order).
  - **Collaboration**: two or more participants (Pools) and the Messages between them. A **Conversation** diagram is a Collaboration that groups message exchanges into hexagons.
  - **Choreography**: the ordered message exchanges themselves, with no pool, no central controller, no shared data.
- **Token**: a theoretical marker used to define behaviour. A Start Event creates one; every token MUST eventually be consumed at an End Event (possibly implicit). Tokens travel Sequence Flows, never Message Flows. Tools need not implement tokens.
- Five element categories: Flow Objects (Events, Activities, Gateways); Data (Data Object, Data Input, Data Output, Data Store); Connecting Objects (Sequence Flow, Message Flow, Association, Data Association); Swimlanes (Pool, Lane); Artifacts (Group, Text Annotation).

## 2. Conformance (§2, pp.1–12)

| Type | Must support |
|---|---|
| Process Modeling | Core (§8), Process (§10), Collaboration and Conversation (§9): notation, structure rules, semantics of §10. Not §13. |
| Process Execution | Operational semantics and Activity lifecycle (§13), the metamodel, import of Process diagrams. Notation not required. |
| BPEL Process Execution | Process Execution plus the WS-BPEL mapping (§14). |
| Choreography Modeling | Core, Choreography (§11), Pools and Message Flow. |
| Complete | All four. |

Process Modeling has three sub-classes (a tool MUST support every listed element and attribute to claim one):

**Descriptive** (Table 2.1): participant (pool) · laneSet/lane · sequenceFlow (unconditional) · messageFlow · exclusiveGateway · parallelGateway · task (None) · userTask · serviceTask · subProcess (expanded, collapsed) · callActivity · dataObject · dataStoreReference · textAnnotation · association / dataAssociation · group · documentation · startEvent: None, Message, Timer · endEvent: None, Message, Terminate.

**Analytic** (Table 2.2) = Descriptive plus: conditional and default sequenceFlow · sendTask · receiveTask · loop and multi-instance activities · inclusiveGateway · eventBasedGateway · default on exclusiveGateway · message on messageFlow · Link catch/throw · start: Signal, Conditional · end: Signal, Error, Escalation · intermediate catch: Message, Timer, Signal, Conditional · intermediate throw: Message, Escalation, Signal · boundary interrupting: Message, Timer, Error, Signal, Conditional · boundary non-interrupting: Message, Timer, Escalation, Signal, Conditional.

**Common Executable** (Tables 2.3–2.4): an executable subset (sequence flows; expanded subProcess; exclusive, parallel, event-based gateways; user and service tasks; callActivity; dataObject; data associations with assignment; None start/end; Message start/end/intermediate; Timer catch; boundary Error; Terminate) with full data and loop attributes. Data types MUST be XML Schema, interfaces WSDL, data access XPath.

**Permitted visual extensions** (§2.2.3, §7.5, §7.7): new markers or indicators; new Artifact shapes that do not clash with any BPMN shape; colour (MAY carry meaning); other line styles that do not clash with a BPMN line style. An extension MUST NOT change the shape of a defined element or marker, and MUST NOT alter the footprint of Events, Activities or Gateways. Extension attributes MUST NOT contradict BPMN semantics.

## 3. Notation rules that apply everywhere (§7.5–7.6, pp.39–42)

- Labels MAY sit inside, above or below a shape, in any direction.
- Fills MAY be white or clear, other colours allowed. Fixed: markers of **throwing** events MUST have a dark fill; **non-initiating** Participant Bands (and return Messages) in choreographies MUST have a light fill.
- Size is free. Lines MAY be black, other colours allowed. The line styles of Sequence Flow, Message Flow and Association MUST NOT be modified or reused.
- Flows MAY attach anywhere on a Flow Object. Recommended: pick one direction for Sequence Flow (left-to-right or top-to-bottom) and draw Message Flows at 90° to it.

**Sequence Flow may connect** (Table 7.3): from Start Event, Task, Sub-Process, Gateway, Intermediate Event → to Task, Sub-Process, Gateway, Intermediate Event, End Event. Nothing flows into a Start Event or out of an End Event. Never across a Sub-Process boundary or a Pool boundary; Lane boundaries may be crossed.

**Message Flow may connect** (Table 7.4): from Pool, Task, Sub-Process, Message Intermediate Event (throw), Message End Event → to Message Start Event, Pool, Task, Sub-Process, Message Intermediate Event (catch). Always between two different Pools. Never to or from a Gateway, Lane, Data Object, Group or Text Annotation.

## 4. Shape and line catalogue

| Element | Drawn as | Ref |
|---|---|---|
| Start Event | circle, single thin line | §10.5.2 |
| Intermediate Event | circle, double thin line | §10.5.4 |
| End Event | circle, single thick line | §10.5.3 |
| Event marker | catch = unfilled icon, throw = filled icon | §10.5 |
| Non-interrupting event | dashed circle (single for Event Sub-Process start, double for boundary) | §10.5 |
| Task | rounded rectangle, single thin line; type icon upper-left | §10.3.3 |
| Sub-Process | same shape; collapsed = boxed `+` bottom-centre; expanded = contents inside | §10.3.5 |
| Event Sub-Process | rounded rectangle, thin **dotted** line | §10.3.5 |
| Transaction | rounded rectangle, **double** thin line | §10.3.5 |
| Call Activity | Task or Sub-Process shape with a **thick** line | §10.3.6 |
| Gateway | diamond, single thin line, marker centred | §10.6 |
| Sequence Flow | solid line, filled arrowhead | §8.4.13 |
| Conditional SF | plus unfilled mini-diamond at the source, only when the source is an Activity | §8.4.13 |
| Default SF | plus a slash near the source | §8.4.13 |
| Message Flow | dashed line, open circle at source, open arrowhead at target; optional envelope on the line | §9.4 |
| Association | dotted line; optional open arrowhead at one or both ends | §8.4.1 |
| Data Association | as a directed Association | §10.4.1 |
| Pool | square-cornered rectangle, solid line; name separated from contents by a line | §9.3 |
| Lane | square-cornered rectangle inside a Pool or Process; name not separated by a line | §10.8 |
| Data Object | page with folded top-right corner (fig); collection = three vertical bars bottom-centre | §10.4.1 |
| Data Input / Output | Data Object with an unfilled / filled block arrow | §10.4.1 |
| Data Store | cylinder (fig) | §10.4.1 |
| Message | envelope, thin line; light fill when it is the return message | §8.4.11 |
| Group | rounded rectangle, dash-dot border `[!]` | §8.4.1 |
| Text Annotation | open rectangle (a bracket), solid line, joined by an Association | §8.4.1 |
| Conversation | hexagon, thin line; Sub-Conversation adds boxed `+`; Call Conversation is thick | §9.5 |
| Conversation Link | double thin line | §9.5.6 |
| Choreography Task | rounded rectangle in bands: participant band(s) top and bottom, name band in the middle | §11.5.1 |

**Activity markers**, grouped and centred at the bottom of the shape (§10.3.3, §10.3.5, Table 12.8): Loop = arrow curling back on itself · Multi-Instance parallel = three vertical bars · Multi-Instance sequential = three horizontal bars · Compensation = two left-pointing triangles · Ad-Hoc = tilde `~` · Collapsed = boxed `+`. Loop and Multi-Instance are mutually exclusive; all other combinations are allowed. Order (fig): loop/MI/compensation, then `+`, then `~`.

**Task type icons**, upper-left (§10.3.3.1; icons other than the envelopes are (fig)): Service = gears · Send = filled envelope · Receive = unfilled envelope (inside a thin circle when it instantiates the Process) · User = person · Manual = hand · Business Rule = table · Script = scroll · none = Abstract Task.

**Event icons** (§10.5.5): Message envelope · Timer clock · Error lightning bolt · Escalation upward arrowhead · Cancel X · Compensation rewind (double left triangle) · Conditional lined page · Link block arrow · Signal triangle · Terminate filled disc · Multiple pentagon · Parallel Multiple unfilled plus.

**Gateway markers** (§10.6): Exclusive = empty or bold X (be consistent within a diagram) · Inclusive = bold circle · Parallel = bold plus · Complex = bold asterisk · Event-Based = pentagon inside a double thin circle; when it instantiates the Process, inside a single circle; instantiating and parallel = unfilled plus inside a single circle.

## 5. Core (§8, pp.47–106)

Required for every conformance type. Packages: Infrastructure, Foundation, Common, Service.

- **Definitions**: outermost element, root of every BPMN file. `name` · `targetNamespace` · `expressionLanguage = http://www.w3.org/1999/XPath` · `typeLanguage = http://www.w3.org/2001/XMLSchema` · `rootElements: RootElement[*]` · `diagrams: BPMNDiagram[*]` · `imports: Import[*]` · `extensions[*]` · `relationships[*]` · `exporter` · `exporterVersion`.
- **Import**: `importType` (XSD 1.0, WSDL 2.0 and BPMN 2.0 MUST be supported; URIs `http://www.w3.org/2001/XMLSchema`, `http://www.w3.org/TR/wsdl20/`, `http://www.omg.org/spec/BPMN/20100524/MODEL`) · `location` · `namespace`.
- **BaseElement** (abstract root of nearly everything): `id` (required if referenced) · `documentation: Documentation[*]` (`text`, `textFormat = text/plain`) · extension hooks. In XML, extensions go in `extensionElements` and foreign-namespace attributes.
- **Extension**: `mustUnderstand: boolean = false` · `definition: ExtensionDefinition`. Standard elements stay intact; only the extension content may be lost in interchange. With XSD interchange the ExtensionDefinition / ExtensionAttributeDefinition / ExtensionAttributeValue classes are not used.
- **Relationship** (link to any external model): `type` · `direction: None | Forward | Backward | Both` · `sources[1..*]` · `targets[1..*]`.
- **RootElement**: abstract; anything owned directly by Definitions and reusable (Process, Collaboration, Choreography, Message, Error, Signal, ItemDefinition, Interface, Resource, Category, EventDefinition, ...).
- **FlowElement** (abstract; anything in a flow): `name` · `categoryValueRef[*]` · `auditing[0..1]` · `monitoring[0..1]`. **FlowNode** (Activity, Choreography Activity, Gateway, Event; the only SF ends): `incoming: SequenceFlow[*]` · `outgoing: SequenceFlow[*]`.
- **FlowElementsContainer** (Process, Sub-Process, Choreography, Sub-Choreography): `flowElements[*]` · `laneSets[*]`. No Choreography Activities in a Process. No Activities, Data Objects or Data Associations in a Choreography, and no LaneSets.
- **SequenceFlow**: `sourceRef: FlowNode` · `targetRef: FlowNode` · `conditionExpression: Expression[0..1]` · `isImmediate: boolean[0..1]`.
  - One source, one target. An Event Sub-Process can be neither.
  - A conditional SF leaving an Activity MUST show the mini-diamond, and the Activity MUST then have at least one other outgoing SF. Leaving a Gateway it MUST NOT show the diamond, and the Gateway MUST NOT be Parallel or Event-Based.
  - Default flow: allowed from Exclusive, Inclusive, Complex Gateways and Activities; taken only when every other condition is false; its own condition is ignored.
  - `isImmediate` false: unmodelled activities MAY happen between the two ends. No value = false for non-executable Processes and Choreographies, true for executable ones; an executable Process MUST NOT set it false.
- **Gateway** (abstract): `gatewayDirection: Unspecified | Converging | Diverging | Mixed = Unspecified`. Converging: several in, at most one out. Diverging: at most one in, several out. Mixed: several of both.
- **Expression**: natural-language text only. **FormalExpression**: `language[0..1]` · `body` · `evaluatesToTypeRef: ItemDefinition`.
- **ItemDefinition**: `itemKind: Information | Physical = Information` · `structureRef[0..1]` · `import[0..1]` · `isCollection = false`.
- **Message**: `name` · `itemRef: ItemDefinition[0..1]`.
- **Error**: `name` · `errorCode` · `structureRef[0..1]`. **Escalation**: `name` · `escalationCode` · `structureRef[0..1]`. In an executable Process the code MUST be given on a throwing event. On a boundary catch it MAY be given: no code catches any, a code catches only the match.
- **Resource**: `name` · `resourceParameters: ResourceParameter[*]` (`name`, `type: ItemDefinition`, `isRequired`).
- **Interface**: `name` · `operations: Operation[1..*]` · `callableElements[*]` · `implementationRef[0..1]`. **Operation**: `name` · `inMessageRef: Message` · `outMessageRef: Message[0..1]` · `errorRef: Error[*]` · `implementationRef[0..1]`. **EndPoint**: extension point for service addresses.
- **Artifacts** (Association, Group, Text Annotation; tools MAY add more): MUST NOT be the source or target of a Sequence Flow or Message Flow.
  - **Association**: `sourceRef` · `targetRef` · `associationDirection: None | One | Both = None` (One = arrowhead at target).
  - **Group**: `categoryValueRef: CategoryValue[0..1]`. Purely visual, may span Pools, does not affect flow. **Category**: `name` · `categoryValue[*]`. **CategoryValue**: `value` · `category[0..1]` · `categorizedFlowElements[*]`.
  - **TextAnnotation**: `text` · `textFormat = text/plain`.
- **Correlation** (§8.4.2) routes a Message to the right instance.
  - *Key-based*: a **CorrelationKey** (`name`, `correlationPropertyRef[*]`) is a composite of **CorrelationProperty** (`name`, `type`, `correlationPropertyRetrievalExpression[1..*]`, each with `messagePath: FormalExpression` and `messageRef: Message`). The first send or receive in a Conversation MUST populate at least one key from its Message; later Messages MUST carry matching values for keys already set.
  - *Context-based*: a Process adds a **CorrelationSubscription** (`correlationKeyRef`, `correlationPropertyBinding[*]`, each with `dataPath: FormalExpression` and `correlationPropertyRef`), so the key is computed from Process data and can change.
  - Keys on a container (Collaboration, Choreography, Conversation Node, Choreography Activity) apply to the Message Flows inside it.

## 6. Process (§10.1–10.2, 10.8–10.11; pp.143–149, 304–311)

**Process** (a CallableElement and FlowElementsContainer): `processType: None | Private | Public = None` · `isExecutable: boolean[0..1]` · `isClosed = false` (true: no unmodelled messages or events may occur) · `supports: Process[*]` (every execution of this one is also valid for those; typically private supports public) · `properties[*]` · `resources: ResourceRole[*]` · `artifacts[*]` · `correlationSubscriptions[*]` · `definitionalCollaborationRef: Collaboration[0..1]` · `auditing`, `monitoring` (empty extension hooks). Runtime attribute `state`.

- A private Process sits in one Pool; Sequence Flow cannot leave the Pool, Message Flow can.
- **Lane**: partitions a Process, running its full length, horizontal or vertical. Its meaning (role, system, department) is the modeller's choice. Lanes nest. **LaneSet**: `name` · `lanes[*]` · `parentLane[0..1]`; a Process may have several LaneSets partitioning the same nodes differently. **Lane**: `name` · `partitionElement[0..1]` · `partitionElementRef[0..1]` · `childLaneSet[0..1]` · `flowNodeRefs: FlowNode[*]`. All Lanes of one LaneSet MUST use the same type of partition element.

## 7. Activities (§10.3, pp.149–202)

**Activity** (abstract): `isForCompensation = false` · `loopCharacteristics[0..1]` · `resources: ResourceRole[*]` · `default: SequenceFlow[0..1]` · `ioSpecification[0..1]` · `properties[*]` · `boundaryEventRefs[*]` · `dataInputAssociations[*]` · `dataOutputAssociations[*]` · `startQuantity = 1` · `completionQuantity = 1` (both ≥ 1). Runtime attribute `state`.

Flow rules (p.151):
- Several incoming SFs = uncontrolled flow: each token starts the Activity separately. Put a Gateway in front to synchronise.
- Several outgoing SFs = one parallel path each.
- No incoming SF: instantiated when the Process is. No outgoing SF: ends a path. Compensation Activities and Event Sub-Processes are exempt from both.
- Any number of Message Flows in and out, to other Pools only.

**Resources**: **ResourceRole**: `resourceRef: Resource[0..1]` or `resourceAssignmentExpression[0..1]` (not both) · `resourceParameterBindings[*]`. Subclasses Performer → HumanPerformer → PotentialOwner.

**Tasks** (atomic). A thick, dotted or double border is reserved, so a Task never has one.

| Task | Meaning | Extra attributes |
|---|---|---|
| Abstract | unspecified | none |
| Service | calls a service or automated application | `implementation = ##WebService` · `operationRef[0..1]` |
| Send | sends a Message, then completes | `messageRef[0..1]` · `operationRef` · `implementation` |
| Receive | waits for a Message | same plus `instantiate = false` |
| User | a person works through a task list | `implementation = ##unspecified` · `renderings[*]`; runtime `actualOwner`, `taskPriority` |
| Manual | done with no engine or application | none |
| Business Rule | calls a rules engine | `implementation = ##unspecified` |
| Script | engine runs a script | `scriptFormat[0..1]` (a MIME type, required if there is a script) · `script[0..1]` |

- `implementation`: `##unspecified`, `##WebService`, or a URI.
- A Receive Task may instantiate the Process only if `instantiate` is true and it has no incoming SF.
- Service Task with an Operation: exactly one InputSet, at most one OutputSet, one Data Input matching the in-Message, one Data Output matching the out-Message if there is one. Send Task: at most one Data Input, matching the Message. Receive Task: at most one Data Output, matching the Message.

**Sub-Process** (also a FlowElementsContainer): `triggeredByEvent = false` · `artifacts[*]`. It is a scope for data, events, exceptions, compensation.
- Collapsed or expanded. Start and End Events inside are optional; an expanded Sub-Process whose activities have no flows runs them all in parallel.
- **Event Sub-Process** (`triggeredByEvent = true`): no incoming or outgoing SF; exactly one Start Event, which MUST have a trigger (Message, Timer, Error, Escalation, Compensation, Conditional, Signal, Multiple, Parallel Multiple). Runs each time the trigger fires while the parent is active. The Start Event's `isInterrupting` decides whether the parent is cancelled.
- **Transaction** (`method`: `##compensate`, `##store`, `##image` or a protocol URI `[!]`). Three outcomes: success (normal outgoing flow, after the protocol confirms every participant); cancel (a Cancel End Event inside, or a protocol cancel message: roll back and compensate, then leave by the boundary Cancel event); hazard (a boundary Error event: interrupt with no compensation). Cancel End Event only inside a Transaction; Cancel boundary event only on one.
- **Ad-Hoc Sub-Process**: `completionCondition: Expression` · `ordering: Parallel | Sequential = Parallel` · `cancelRemainingInstances = true`. Activities with no required order, each performed any number of times, chosen by the performers. MUST contain Activities; MAY contain Data Objects, Sequence Flows, Associations, Data Associations, Groups, Gateways, Intermediate Events, Message Flow ends; MUST NOT contain Start Events, End Events, Conversations, Choreography Activities.

**Call Activity**: `calledElement: CallableElement[0..1]`, a Process or a GlobalTask only. Its io specification MUST match the called element's exactly. Its ResourceRoles override the called element's. Errors and escalations propagate from the called element to the Call Activity's boundary. A Call Activity for a Global Task shows that task type's icon.
- **CallableElement**: `name` · `supportedInterfaceRefs[*]` · `ioSpecification[0..1]` · `ioBinding[*]` (`inputDataRef`, `outputDataRef`, `operationRef`).
- **GlobalTask**: `resources[*]`. Kinds: GlobalUserTask, GlobalManualTask, GlobalScriptTask, GlobalBusinessRuleTask.

**Loops** (runtime `loopCounter`):
- **StandardLoopCharacteristics**: `testBefore = false` · `loopMaximum[0..1]` · `loopCondition[0..1]`. Repeats while the condition is true.
- **MultiInstanceLoopCharacteristics**: `isSequential = false` · `loopCardinality[0..1]` · `loopDataInputRef[0..1]` · `loopDataOutputRef[0..1]` · `inputDataItem[0..1]` · `outputDataItem[0..1]` · `behavior: None | One | All | Complex = All` · `complexBehaviorDefinition[*]` (`condition`, `event: ImplicitThrowEvent`) · `completionCondition[0..1]` · `oneBehaviorEventRef[0..1]` · `noneBehaviorEventRef[0..1]`.
  - `loopCardinality` or the loop data input MUST be given: one instance per unit or per collection item, evaluated once.
  - `completionCondition` true: cancel the remaining instances and continue.
  - `behavior`: None = throw the event at every instance completion; One = at the first; All = never; Complex = per the definitions. Thrown events can be caught on the activity's own boundary.
  - Runtime: `numberOfInstances`, `numberOfActiveInstances`, `numberOfCompletedInstances`, `numberOfTerminatedInstances`.

## 8. Data (§10.4, pp.202–232)

- **ItemAwareElement** (Data Object, Data Object Reference, Data Store Reference, Property, Data Input, Data Output): `itemSubjectRef: ItemDefinition[0..1]` · `dataState: DataState[0..1]` (`name`; meaning is the modeller's).
- **DataObject**: `isCollection = false`. Lives in a Process or Sub-Process, created and destroyed with it. Visible to its parent and everything nested below, never to the level above. **DataObjectReference**: `dataObjectRef`; shows the same object again, possibly in another state; label `Name [State]`.
- **DataStore** (global, outlives the Process): `name` · `capacity[0..1]` · `isUnlimited = false`. Drawn through a **DataStoreReference** (`dataStoreRef`).
- **Property**: `name`. Not drawn. Only Processes, Activities and Events have them; visible to the owner and, for a Process or Sub-Process, everything inside it.
- **InputOutputSpecification**: `dataInputs[*]` · `dataOutputs[*]` · `inputSets[1..*]` · `outputSets[1..*]`. Only Tasks and CallableElements define one. An embedded Sub-Process MUST NOT, except indirectly through multi-instance.
  - **DataInput** / **DataOutput**: `name` · `isCollection = false`, plus the sets that use it.
  - **InputSet**: `dataInputRefs[*]` · `optionalInputRefs[*]` · `whileExecutingInputRefs[*]` · `outputSetRefs[*]`. **OutputSet**: mirror image. Every input or output MUST belong to at least one set.
  - Data Inputs and Outputs of the top-level Process may be drawn, and MUST NOT be the end of a Data Association in the model.
- **DataAssociation** (owned by an Activity or Event): `sourceRef: ItemAwareElement[*]` · `targetRef: ItemAwareElement` · `transformation: Expression[0..1]` · `assignment[*]` (`from`, `to`). Subclasses **DataInputAssociation**, **DataOutputAssociation**.
  - Source and target MUST share an ItemDefinition unless there is a transformation. With no transformation there is exactly one source.
  - No token travels a Data Association. Drawing it is optional.
  - Shortcut: a Data Object attached to a Sequence Flow stands for an output association from the flow's source plus an input association to its target.
- **Execution** (§10.4.2):
  - Start of an Activity: InputSets are tried in order and the first whose inputs are all available is used; if none, the Activity waits.
  - End of an Activity: the associations of the chosen OutputSet copy data back out.
  - Events have no sets and never wait. A throw event fills its Data Input, then the thrown item. A catch event fills its Data Output from the trigger, then runs its associations.
  - One association runs as: transformation result to target, else each assignment, else a plain copy.
- **Events carrying data** (Message, Error, Escalation, Signal): one Data Input (throw) or Data Output (catch) per EventDefinition, matched by order, with an equivalent ItemDefinition.
- **XPath functions** (§10.4.3): `getDataObject`, `getDataInput`, `getDataOutput`, `getProcessProperty`, `getActivityProperty`, `getEventProperty`, `getProcessInstanceAttribute`, `getActivityInstanceAttribute`, `getChoreographyInstanceAttribute`. Arguments MUST be literal strings; errors return an empty node set.

## 9. Events (§10.5, pp.232–286)

Classes: **Event**: `properties[*]`. **CatchEvent**: `eventDefinitions[*]` · `eventDefinitionRefs[*]` · `dataOutputs[*]` · `dataOutputAssociations[*]` · `outputSet[0..1]` · `parallelMultiple = false`. **ThrowEvent**: the same with inputs. No definition = None event; more than one = Multiple. **StartEvent**: `isInterrupting = true` (Event Sub-Process starts only). **BoundaryEvent**: `attachedToRef: Activity` · `cancelActivity = true`. **ImplicitThrowEvent**: not drawn, used by multi-instance.

**Where each type may appear** (Table 10.93):

| Type | Start, top level | Start, Event Sub-Process, interrupting | ...non-interrupting | Intermediate catch | Boundary, interrupting | ...non-interrupting | Intermediate throw | End |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| None | ✓ | | | | | | ✓ | ✓ |
| Message | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Timer | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| Conditional | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| Signal | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Multiple | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Parallel Multiple | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| Escalation | | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ |
| Error | | ✓ | | | ✓ | | | ✓ |
| Compensation | | ✓ | | | ✓ | | ✓ | ✓ |
| Cancel | | | | | ✓ | | | ✓ |
| Link | | | | ✓ | | | ✓ | |
| Terminate | | | | | | | | ✓ |

A Start Event inside an ordinary Sub-Process is None only. Error always interrupts. For Compensation, interrupting does not apply (drawn solid).

**EventDefinitions**:

| Definition | Attributes | Rule |
|---|---|---|
| Message | `messageRef[0..1]` · `operationRef[0..1]` | both required when executable |
| Timer | `timeDate` or `timeCycle` or `timeDuration` | exactly one; ISO 8601 |
| Conditional | `condition: Expression` | formal when executable; fires again only after going false then true; a top-level start condition MUST NOT read Process data |
| Signal | `signalRef[0..1]` | broadcast; no named target |
| Error | `errorRef[0..1]` | |
| Escalation | `escalationRef[0..1]` | |
| Compensation | `activityRef[0..1]` · `waitForCompletion = true` | see below |
| Link | `name` (required) · `sources` · `target` | see below |
| Cancel, Terminate | none | |

**Start Event**: optional at every level, but if a level has an End Event it MUST have a Start Event, and vice versa. No incoming SF; at least one outgoing; outgoing SFs carry no condition. May receive Message Flows, never send. Several Start Events are alternatives: each occurrence makes a new instance. To require several triggers for one instance, use Parallel Multiple. Without Start Events, every flow object with no incoming SF starts when the Process does.

**End Event**: no outgoing SF. May send Message Flows, never receive. If it has outgoing Message Flows its result MUST be Message, or Multiple when there are several. A Process ends only when all tokens are consumed.
- Error: terminates all activity in the Sub-Process and propagates to the nearest enclosing boundary catch with the same or no code. Unhandled: unspecified.
- Escalation: propagates the same way; other threads continue.
- Cancel: only in a Transaction. Signal: broadcast. Terminate: ends everything in the Process or Sub-Process at once, with no compensation and no event handling.

**Intermediate Event, in the flow**: one or more incoming and one or more outgoing SFs. Catch: the token waits for the trigger. Throw: fires and continues. Error and Cancel are not allowed here. A Message event has at most one Message Flow, in or out.

**Boundary Event**: catch only, attached anywhere on an Activity's edge. No incoming SF; at least one outgoing (a Compensation boundary event instead has no SF and uses an Association to its Compensation Activity). Interrupting: the Activity is terminated and the token takes the exception flow. Non-interrupting: the Activity continues and a parallel token leaves the event; end that path on its own, since merging it back needs care.

**Link**: a go-to within one Process level. The source is a throw event with an incoming SF only; the target is a catch event with an outgoing SF only; they share a name. Many sources may jump to one target, never one source to many targets.

**Compensation**: undoes work that completed successfully (§10.7, §13.5.5).
- A handler is either a Compensation Activity (`isForCompensation`, compensation marker, outside the normal flow) joined by an Association to a Compensation boundary event, or a Compensation Event Sub-Process, which sees a snapshot of its parent's data taken at completion.
- A throw (intermediate or end) names an Activity or names none. Named: that Activity is compensated if it completed and is visible (same Sub-Process level, or the thrower sits in a Compensation Event Sub-Process of the enclosing Sub-Process). Unnamed: every completed visible Activity, in reverse order of execution.
- Only completed Activities compensate; for a failed or running one it is a no-op. `waitForCompletion` true: the thrower waits for the handlers.
- If a Sub-Process has no handler for a thrown error, the default is to compensate its completed contents.

**Trigger delivery** (§10.5.1): Message = published across Pools, correlated to an instance. Signal = broadcast everywhere. Timer, Conditional = implicit. Error, Escalation = propagated outward to the innermost enclosing catch; Error suspends the thrower, Escalation does not. Cancellation terminates what runs and compensates what completed.

**Event Sub-Process against boundary event for the same trigger**: the Event Sub-Process runs first, inside the Sub-Process's data context; the boundary event fires only if it re-throws. For one trigger, at most one interrupting handler; any number of non-interrupting ones.

## 10. Gateways (§10.6, §13.4; pp.286–301, 434–439)

A Gateway MUST have several incoming or several outgoing SFs. Recommended: one function per Gateway.

| Gateway | Split | Join | Attributes |
|---|---|---|---|
| Exclusive | conditions evaluated in order; first true wins; else default; else exception | each token passes straight through | `default[0..1]` |
| Inclusive | every true condition gets a token; none true = default; else exception | waits for every token that can still arrive (rule below) | `default[0..1]` |
| Parallel | a token on every outgoing SF, no conditions | waits for one token on every incoming SF | none |
| Complex | as Inclusive | `activationCondition` decides; then resets | `activationCondition[0..1]` · `default[0..1]`; runtime `activationCount`, `waitingForStart` |
| Event-Based | the first event to occur picks the path | pass-through | `instantiate = false` · `eventGatewayType: Exclusive | Parallel = Exclusive` |

- **Inclusive join** (§13.4.3) fires when at least one incoming SF has a token and no token elsewhere in the diagram can still reach an *empty* incoming SF without also being able to reach a *non-empty* one, by paths that do not pass through this Gateway. It then consumes one token from each non-empty incoming SF.
- **Complex**: waits until `activationCondition` is true, consumes a token from each incoming SF that has one, emits like an Inclusive split, then waits for reset (the remaining expected tokens, by the Inclusive rule), consumes them and returns to the start state `[!]`.
- **Event-Based**:
  - Two or more outgoing SFs, none with a condition.
  - Targets: catch events (Message, Timer, Signal, Conditional, or a Multiple of those) or Receive Tasks. Message events and Receive Tasks are not mixed.
  - Targets have no other incoming SF. Receive Tasks used this way have no boundary events.
  - `instantiate` true requires no incoming SF, and starts the Process on the first event.
  - `Parallel` is allowed only when instantiating: every event of the configuration is then required, all sharing correlation data.

## 11. Execution semantics (§13, pp.425–444)

Required only for Process Execution conformance.

- **Not executable** (engines MAY ignore): Manual Task, Abstract Task, DataState, Ad-Hoc Process, physical ItemDefinitions, the while-executing input and output sets, `isClosed`, `isImmediate`.
- **Instantiation**: by a Start Event, or by an Event-Based Gateway or Receive Task with `instantiate` true and no incoming SF. A start that belongs to a Conversation which already has an instance (same correlation data) is routed to that instance.
- **Completion**: no tokens left, no active Activity, and every event of an instantiating parallel Event-Based Gateway has occurred.
- **Activity lifecycle** (fig 13.2):
  - Inactive → Ready, when `startQuantity` tokens have arrived.
  - Ready → Active, when an InputSet is available.
  - Active → Completing, while it waits for running non-interrupting handlers.
  - Completing → Completed, emitting `completionQuantity` tokens on each outgoing SF.
  - Completed → Compensating → Compensated.
  - Error interrupt: → Failing → Failed. Any other interrupt: → Terminating → Terminated.
  - Withdrawn: it lost the race after an Event-Based Gateway.
- **Implicit gateways on an Activity**: several incoming SFs behave as an Exclusive merge. Unconditional outgoing SFs behave as a Parallel split, conditional ones as an Inclusive split.
- **Tasks**: Service = invoke the Operation, a fault is an interrupting error. Send = send. Receive = wait. User = wait for the person. Business Rule and Script = run to completion. Abstract = completes at once.
- **Sub-Process**: starts at its single None Start Event, or at every node with no incoming SF. Completes when no tokens and no active Activities remain. A called Process ignores its triggered Start Events.
- **Ad-Hoc**: activities with no incoming SF are enabled; `completionCondition` is evaluated after each completion.
- **Event Sub-Process**: can start only while the parent is active. The parent stays in Completing until running handlers finish. An interrupting handler moves the parent to Failing (error) or Terminating (anything else).
- **Default compensation order**: the reverse of execution, honouring Sequence Flow and data dependencies. Parallel multi-instance instances may be compensated in parallel.

## 12. Collaboration, Conversation, Choreography (§9, §11; pp.107–142, 315–366)

**Collaboration**: `name` · `participants[*]` · `messageFlows[*]` · `artifacts[*]` · `conversations: ConversationNode[*]` · `conversationLinks[*]` · `correlationKeys[*]` · `choreographyRef[*]` · `participantAssociations[*]` · `messageFlowAssociations[*]` · `conversationAssociations[*]` · `isClosed = false`.

**Participant** (drawn as a Pool): `name` · `processRef: Process[0..1]` · `interfaceRefs[*]` · `endPointRefs[*]` · `participantMultiplicity[0..1]` (`minimum = 0`, `maximum = 1`). Stands for a **PartnerEntity** (a specific company), a **PartnerRole** (buyer, seller), or both.
- A Pool may hold a Process (white box) or nothing (black box; Message Flows attach to its edge).
- One Pool per diagram MAY be drawn without a boundary.
- A Pool runs the full length of the diagram.
- A multi-instance participant (`maximum` of 2 or more) shows three vertical bars bottom-centre.

**MessageFlow**: `name` · `sourceRef`, `targetRef: InteractionNode` (Participant, Activity or Event) · `messageRef[0..1]`.

**Association classes** map inner to outer when one diagram reuses another: **ParticipantAssociation** (`innerParticipantRef`, `outerParticipantRef`), **MessageFlowAssociation**, **ConversationAssociation**.

**Conversation diagram**: a Collaboration view in which hexagons group Message Flows that share a correlation.
- **ConversationNode** (abstract): `name` · `participantRefs[2..*]` · `messageFlowRefs[*]` · `correlationKeys[*]`. Kinds: **Conversation** (atomic) · **SubConversation** (`conversationNodes[*]`) · **CallConversation** (`calledCollaborationRef`: a Collaboration or GlobalConversation, never a Choreography; `participantAssociations[*]`).
- **GlobalConversation**: a reusable Collaboration with no Conversation Nodes.
- **ConversationLink**: `name` · `sourceRef` · `targetRef`; exactly one end MUST be a Conversation Node.

**Choreography** (is a Collaboration and a FlowElementsContainer). No Pools, Lanes, Data Objects or Data Stores. Sequence Flows connect only Events, Gateways and Choreography Activities.
- **ChoreographyActivity** (abstract): `participantRefs[2..*]` · `initiatingParticipantRef` · `loopType: None | Standard | MultiInstanceSequential | MultiInstanceParallel = None` · `correlationKeys[*]`.
- **ChoreographyTask**: `messageFlowRef[1..*]`. One or two Messages between two participants. The initiator's band is unshaded, the other band light-filled. A Message envelope may be tethered to its sender's band: unfilled for the initiating Message, light-filled for the return.
- **SubChoreography** (`artifacts[*]`): collapsed shows `+` in the name band. Further participants add bands alternately above and below.
- **CallChoreography** (`calledChoreographyRef`, `participantAssociations[*]`): thick border. **GlobalChoreographyTask**: `initiatingParticipantRef`; contains no flow elements.
- Loop and multi-instance markers sit in the name band; a multi-instance participant shows three bars in its band.
- **Sequencing rule**: the initiator of a Choreography Activity MUST have taken part in the one before it, or it cannot know when to send.
- **Events allowed**:
  - Start: None, Timer, Conditional, Signal, Multiple.
  - End: None, Terminate.
  - Intermediate in the flow: None, Timer, Conditional, Link, Signal (catch), Multiple.
  - Boundary: Message (on a Choreography Task, attached to the receiver's band), Timer, Cancel, Compensation, Conditional, Signal, Multiple.
  - Not allowed: Message Start, End and in-flow events (use a Choreography Task); Error; Escalation; throwing Cancel, Compensation or Signal.
- **Gateways**:
  - Exclusive and Inclusive: the condition data MUST have travelled in an earlier Message seen by every participant the gateway affects, and the initiators after the gateway MUST have seen it.
  - Event-Based: after the gateway, either all senders are the same or all receivers are. Timer and Signal events are allowed there, Message events are not.
  - Parallel and Inclusive: every sender after the gateway MUST have taken part in every activity just before it.
  - Complex: no stated constraints.
- **Choreography inside a Collaboration**: it sits between the Pools; Message Flows pass through the Choreography Tasks; band names are optional because the Pools carry them. `isClosed` MUST match in both.

## 13. Diagram interchange and files (§12, §15, Annex B; pp.367–424, 475–497)

- DI stores only what the model cannot: position, size, routing. Colour is not interchanged. Rendering needs both the DI and the model. DI does not make a diagram valid.
- **BPMNDiagram**: `name` · `documentation` · `resolution` · `plane: BPMNPlane[1]` · `labelStyle: BPMNLabelStyle[*]`. One file may hold many diagrams. A diagram may show part of a model, and an element may appear in several diagrams, but only once per diagram (Participant Bands excepted).
- **BPMNPlane**: `bpmnElement` = a Process, Sub-Process, Ad-Hoc Sub-Process, Transaction, Collaboration, Choreography or Sub-Choreography. Origin top-left, x to the right, y downward, positive coordinates only. Its children form one flat ordered list, never nested; the order is the z-order, later on top.
- **BPMNShape**: `bpmnElement` · `bounds: Bounds[1]` (`x`, `y`, `width`, `height`; top-left corner) · `label[0..1]` · `isHorizontal` (Pools, Lanes) · `isExpanded` (Sub-Process kinds, Call Activity, Sub- and Call Choreography; absent = collapsed `[!]`) · `isMarkerVisible` (Exclusive Gateway X) · `participantBandKind` · `isMessageVisible` · `choreographyActivityShape` (required on a band).
- **BPMNEdge**: `bpmnElement` · `waypoint: Point[2..*]` · `label[0..1]` · `sourceElement`, `targetElement` (only when the drawn end differs from the model end, such as a Message Flow drawn to a black-box Pool edge or a Data Association drawn to an Activity edge) · `messageVisibleKind: initiating | non_initiating` (envelope at the midpoint; unshaded or shaded).
- **BPMNLabel**: `bounds[0..1]` · `labelStyle[0..1]`. Present = visible. Text = the element's `name`. **BPMNLabelStyle**: `font: Font` (`name`, `size`, `isBold`, `isItalic`, `isUnderline`, `isStrikeThrough`).
- **ParticipantBandKind**: `top_initiating` · `middle_initiating` · `bottom_initiating` · `top_non_initiating` · `middle_non_initiating` · `bottom_non_initiating`. Each band is its own BPMNShape referencing the Participant. An edge never ends on a band.
- Everything else about a depiction is resolved from the model: event type from its EventDefinitions, dashed border from `cancelActivity` / `isInterrupting`, markers from `loopCharacteristics` / `isForCompensation`, thick border from the element being a Call Activity, the slash from `default`.
- A collapsed Sub-Process's content goes on a second diagram whose plane references that Sub-Process.
- The Data-Object-to-Sequence-Flow shortcut is the one edge with no `bpmnElement`: its `targetElement` is the Sequence Flow's edge.

**Files** (§15):
- The root of every file is `definitions`, which MUST declare a `targetNamespace`.
- A model may span files; everything used MUST be imported.
- References are by `id`: IDREF within a file, QName across files.
- Incomplete models may be interchanged: importers disregard missing required attributes and unmet minimum cardinalities.
- Machine-readable files: OMG dtc/2010-05-04 (`BPMN20.xsd`, CMOF/XMI, XSLT both ways).

| Namespace | URI |
|---|---|
| model | `http://www.omg.org/spec/BPMN/20100524/MODEL` |
| `bpmndi` | `http://www.omg.org/spec/BPMN/20100524/DI` |
| `dc` | `http://www.omg.org/spec/DD/20100524/DC` |
| `di` | `http://www.omg.org/spec/DD/20100524/DI` |

**WS-BPEL mapping** (§14, pp.445–474). Only sound, block-structured Processes map directly (no deadlock, never two tokens on one SF).

| BPMN | WS-BPEL |
|---|---|
| Process | `process` |
| Service or Send Task | `invoke` |
| Receive Task, Message catch | `receive` |
| Abstract Task | `empty` |
| Sub-Process | `scope` |
| Event Sub-Process | event, fault or compensation handlers |
| Standard loop | `while` / `repeatUntil` |
| Multi-instance | `forEach` |
| Timer | `wait` |
| Exclusive block | `if` |
| Event-Based block | `pick` |
| Parallel or Inclusive block | `flow` (with links) |
| Plain sequence | `sequence` |
| Error End | `throw` |
| Terminate | `exit` |
| Compensation throw | `compensate` / `compensateScope` |
| Data Objects, Properties | variables |
| Correlation keys | `correlationSet` |

Unstructured or interleaved loops need derived processes. No mapping is given for User, Manual, Script and Business Rule Tasks, Call Activity, Complex Gateway, Signal, Conditional, Escalation, Link and Cancel events, Transactions, or Ad-Hoc Sub-Processes.

**Annexes**: A = changes from 1.2 (adds Choreography and Conversation diagrams, non-interrupting events, Event Sub-Processes, a formal metamodel and interchange formats; Reference Tasks become Global Tasks). B = the DC/DI base model (non-normative). C = glossary.

## 14. Where the spec contradicts itself

Stated as printed; do not treat either side as settled.

1. **Group border**: text says "solid dashed line"; the figures show dash-dot (§8.4.1).
2. **`isExpanded` default**: collapsed tables say absent = collapsed; three expanded tables (12.13, 12.15, 12.20) say absent = expanded.
3. **Lane and Pool orientation**: Tables 12.25–12.26 test `isVertical`; the attribute defined and used in the examples is `isHorizontal`.
4. **Complex Gateway reset**: §10.6.5 says no token is produced on reset; §13.4.5 says outgoing conditions are evaluated and tokens are produced. Attribute named `activationCondition` in §10.6.5, `activationExpression` in §13.4.5.
5. **Compensating a multi-instance**: §10.7.2 invokes a boundary handler once per instance; §13.5.5 says once for all instances.
6. **Transaction `method`**: Table 10.21 gives `##compensate | ##store | ##image`; the schema gives `Compensate | Image | Store`, default `Compensate`.
7. **`implementation` default**: printed `##webService` in tables, `##WebService` in the schema.
8. **Multi-instance `behavior`** default is printed `all`; literals are capitalised.
9. **None Intermediate Event**: throw in Tables 10.89 and 10.93, called catch in the "None Event" text (p.271).
10. **Non-interrupting boundary types**: p.276 and §13.5.3 list only Message, Signal, Timer, Conditional; Tables 10.90–10.93 also allow Escalation, Multiple, Parallel Multiple.
11. **Link direction**: p.258 words source and target loosely; pp.266–267 define source = throw, target = catch. `LinkEventDefinition.sources`/`target` multiplicities differ between Table 10.98 and the schema.
12. **Sub-Process Start Events**: §13.3.4 forbids non-None Start Events in a Sub-Process, then describes Start Events targeted by outside flows; §13.2 forbids a None Start Event in a "global Process", which §13.3.4 then relies on.
13. **`isExecutable` default**: §10.9 says both false and true; the schema gives none.
14. **Participant multiplicity**: `maximum` defaults to 1, yet the marker rule fires when it is "not set".
15. **Choreography Task messages**: Table 11.2 says `[1..*]`; text and schema say one or two.
16. **Choreography timers and Event-Based Gateways**: absolute timers are said to need no participant relationship in normal flow, but carry the same MUSTs as relative timers elsewhere; §11.7.2 allows only Timer and Signal after an Event-Based Gateway while Table 11.7 also allows Conditional.
17. **Choreography Inclusive merge** rule is garbled ("participate in the Gateway immediately preceding the Gateway"); read here as the activities preceding it.
18. **`MessageVisibleKind`** literal is spelled three ways; the schema's `non_initiating` is used here.
19. **Collapsed Event Sub-Process**: text and Table 12.16 say its start event icon appears upper-left; Figure 10.30 does not show it.
20. **Clause numbering**: cross-references in clauses 2 and 6 are off by one (they call Execution Semantics "Clause 14", DI "Clause 13").
21. Minor: `Import.location` optional in the table, required in the schema; `textFormat` default printed `textplain` in the schema; the Activity attribute is spelled `completetionQuantity` in the schema listing; several attributes have no printed multiplicity.
