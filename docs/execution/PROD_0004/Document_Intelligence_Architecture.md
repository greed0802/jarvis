# Document Intelligence Architecture

High-level architecture showing components organization:

```
                  +--------------------------------+
                  |       WorkspaceAssistant       |
                  +--------------------------------+
                                  │
                                  ▼
                  +--------------------------------+
                  |        DocumentResolver        |
                  +--------------------------------+
                                  │
                                  ▼
             +──────────────────────────────────────────+
             |        DocumentIntelligenceEngine        |
             +──────────────────────────────────────────+
               │        │           │          │       │
               ▼        ▼           ▼          ▼       ▼
           Registry  Classifier  RelEngine  CompEng  RecEngine
```
