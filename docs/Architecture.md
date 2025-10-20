# Architecture — comics-suite

Date: 2025-10-19

```mermaid
flowchart LR
  A[ComicVine]-->CORE
  B[Metron]-->CORE
  C[GCD]-->CORE
  CORE(comicbook-core)-->DOCTOR[cbz-doctor]
  DOCTOR-->ORG[comic-file-organizer]
  ORG-->M[Mylar3]
```
