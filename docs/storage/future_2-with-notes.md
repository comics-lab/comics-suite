graph TD

    %% Main storage pool on the new core server
    subgraph POOL["📦 Main Storage Pool (Core Server)"]
        POOL_TYPE["ZFS / Btrfs Pool<br/>RAIDZ2 / RAID10 / RAID1+Spare"]

        DISK14A["14TB Disk A"]
        DISK14B["14TB Disk B"]
        DISK9A["9TB Disk A"]
        DISK9B["9TB Disk B"]
        DISK7["7TB Disk (optional)"]

        DISK14A --> POOL_TYPE
        DISK14B --> POOL_TYPE
        DISK9A --> POOL_TYPE
        DISK9B --> POOL_TYPE
        DISK7  --> POOL_TYPE
    end

    %% Datasets / subvolumes / shares
    subgraph DATASETS["Logical Datasets / Shares"]
        DS_COMICS["comics/primary<br/>(replaces /mnt/fearless, /mnt/longbox, /mnt/shortbox, /mnt/DC)"]
        DS_ARCS["comics/arcs<br/>(replaces /mnt/arcs)"]
        DS_PUBS["comics/pubs<br/>(replaces /mnt/pubs, /mnt/Marvel)"]
        DS_HOME["users/home"]
        DS_BACKUPS["backups/lab_nodes"]
    end

    POOL_TYPE --> DS_COMICS
    POOL_TYPE --> DS_ARCS
    POOL_TYPE --> DS_PUBS
    POOL_TYPE --> DS_HOME
    POOL_TYPE --> DS_BACKUPS

    %% Services running on the core server
    subgraph SERVICES["🧩 Core Services (Docker / Native)"]
        S_KAVITA["Kavita"]
        S_MYLAR["Mylar3"]
        S_PORTAINER["Portainer"]
        S_DB["Postgres / MariaDB"]
        S_EXPORT["NFS + SMB exports"]
        S_MON["Monitoring / Metrics"]
        S_HA["Home Assistant (optional - VM or container)"]
    end

    DS_COMICS --> S_KAVITA
    DS_COMICS --> S_MYLAR
    DS_ARCS --> S_MYLAR
    DS_PUBS --> S_KAVITA

    DS_HOME --> S_EXPORT
    DS_BACKUPS --> S_EXPORT

    %% Clients consuming exports
    BEAST["The Beast<br/>(workstation)"]
    ZIMA["Zima"]
    HAWK["Hawkeye"]
    HIPPY["Hippy"]
    SWEETPEA["Sweetpea"]

    S_EXPORT --> BEAST
    S_EXPORT --> ZIMA
    S_EXPORT --> HAWK
    S_EXPORT --> HIPPY
    S_EXPORT --> SWEETPEA

Oh, this is the fun part. Let’s time-skip a bit and draw what this should look like once The Beast is freed and you’ve got a proper central server.

I’ll give you:
	1.	A “Future Physical Topology” Mermaid diagram
	2.	A “Future Logical Storage & Services” diagram
	3.	Notes explaining what’s what and how it connects to the plan

You can drop these straight into a README.

⸻
1️⃣ Future Physical / Connection Topology (Mermaid)

graph TD
    %% Core idea: New NAS/mini-server is the storage + service hub.
    %% The Beast + lab nodes become clients instead of storage hosts.

    subgraph CORE["🌐 Future Core Server (NAS / Mini PC)"]
        CORE_CPU["CPU: N100 / i3-class (no transcoding needed)"]
        CORE_RAM["RAM: 32GB"]
        CORE_NET["2.5GbE (or better)"]
        CORE_OS["OS: TrueNAS SCALE / Unraid / OMV"]

        subgraph CORE_DRIVES["Internal Storage (Direct SATA/NVMe)"]
            CORE_NVME1["NVMe0: OS + Docker + DBs"]
            CORE_NVME2["NVMe1: cache / metadata (optional)"]

            CORE_HDD1["HDD1: 14TB (from DAS bay 1)"]
            CORE_HDD2["HDD2: 14TB (from DAS bay 2)"]
            CORE_HDD3["HDD3: 9TB (from /mnt/arcs)"]
            CORE_HDD4["HDD4: 9TB (from /mnt/pubs)"]
            CORE_HDD5["HDD5: 7TB (from /mnt/data, optional)"]
            CORE_HDD6["HDD6: 4TB/4TB (from 'grackle', optional)"]
        end
    end

    %% Network fabric
    SWITCH["🕸️ LAN Switch / Router<br/>1G / 2.5G"]
    CORE_NET --> SWITCH

    %% Existing lab nodes become clients only
    subgraph LAB["Existing Lab Nodes (Clients)"]
        BEAST["The Beast<br/>Workstation only<br/>(no direct USB storage)"]
        ZIMA["Zima (Zimaboard)"]
        HAWK["Hawkeye (Pi 4B+)"]
        HIPPY["Hippy (old laptop)"]
        SWEETPEA["Sweetpea (Pi B+)"]
    end

    SWITCH --> BEAST
    SWITCH --> ZIMA
    SWITCH --> HAWK
    SWITCH --> HIPPY
    SWITCH --> SWEETPEA

    %% External USB enclosures in the future
    subgraph LEGACY_USB["Legacy USB/DAS (After Migration)"]
        DAS["Former DAS Enclosure<br/>(empty or repurposed)"]
        USB_SINGLE["Any leftover USB drives<br/>(used only as cold backup or offline)"]
    end

    %% After migration, USB/DAS are NOT in the main data path
    BEAST -.optional offline backup access .-> LEGACY_USB

⸻

2️⃣ Future Logical Storage & Services (Mermaid)

graph TD

    %% Main storage pool on the new core server
    subgraph POOL["📦 Main Storage Pool (Core Server)"]
        POOL_TYPE["ZFS / Btrfs Pool<br/>RAIDZ2 / RAID10 / RAID1+Spare"]

        DISK14A["14TB Disk A"]
        DISK14B["14TB Disk B"]
        DISK9A["9TB Disk A"]
        DISK9B["9TB Disk B"]
        DISK7["7TB Disk (optional)"]

        DISK14A --> POOL_TYPE
        DISK14B --> POOL_TYPE
        DISK9A --> POOL_TYPE
        DISK9B --> POOL_TYPE
        DISK7  --> POOL_TYPE
    end

    %% Datasets / subvolumes / shares
    subgraph DATASETS["Logical Datasets / Shares"]
        DS_COMICS["comics/primary<br/>(replaces /mnt/fearless, /mnt/longbox, /mnt/shortbox, /mnt/DC)"]
        DS_ARCS["comics/arcs<br/>(replaces /mnt/arcs)"]
        DS_PUBS["comics/pubs<br/>(replaces /mnt/pubs, /mnt/Marvel)"]
        DS_HOME["users/home"]
        DS_BACKUPS["backups/lab_nodes"]
    end

    POOL_TYPE --> DS_COMICS
    POOL_TYPE --> DS_ARCS
    POOL_TYPE --> DS_PUBS
    POOL_TYPE --> DS_HOME
    POOL_TYPE --> DS_BACKUPS

    %% Services running on the core server
    subgraph SERVICES["🧩 Core Services (Docker / Native)"]
        S_KAVITA["Kavita"]
        S_MYLAR["Mylar3"]
        S_PORTAINER["Portainer"]
        S_DB["Postgres / MariaDB"]
        S_EXPORT["NFS + SMB exports"]
        S_MON["Monitoring / Metrics"]
        S_HA["Home Assistant (optional - VM or container)"]
    end

    DS_COMICS --> S_KAVITA
    DS_COMICS --> S_MYLAR
    DS_ARCS --> S_MYLAR
    DS_PUBS --> S_KAVITA

    DS_HOME --> S_EXPORT
    DS_BACKUPS --> S_EXPORT

    %% Clients consuming exports
    BEAST["The Beast<br/>(workstation)"]
    ZIMA["Zima"]
    HAWK["Hawkeye"]
    HIPPY["Hippy"]
    SWEETPEA["Sweetpea"]

    S_EXPORT --> BEAST
    S_EXPORT --> ZIMA
    S_EXPORT --> HAWK
    S_EXPORT --> HIPPY
    S_EXPORT --> SWEETPEA

⸻

3️⃣ Explanatory Notes (for the README)

You can drop something like this under the diagrams:

🧠 High-Level Design
	•	The new Core Server (NAS or mini PC) becomes the central storage + services node.
	•	All big disks (the two 14TB, the 9TBs, and optionally the 7TB + 4TBs) move inside the core server on SATA, no more USB bottlenecks.
	•	The system uses one main pool (ZFS or Btrfs), carved into datasets/subvolumes that map to your current layout:
	•	comics/primary → replaces /mnt/fearless, /mnt/DC, /mnt/longbox, /mnt/shortbox
	•	comics/arcs → replaces /mnt/arcs
	•	comics/pubs → replaces /mnt/pubs + /mnt/Marvel
	•	users/home → replaces home data scattered across Beast + NVMe
	•	backups/lab_nodes → target for backing up Pi, Zima, Hippy, etc.

⸻

📦 Storage Strategy Notes
	•	No USB in the main data path
	•	USB DAS and external drives become optional backup/cold storage only.
	•	RAID level:
	•	ZFS: RAIDZ2 (if you have 5–6 disks) or mirrored vdevs.
	•	Btrfs: RAID10 or RAID1C3 depending on how many disks you commit.
	•	The two 14TB drives are your “anchor” capacity; the 9TB and 7TB drives round out the pool.
	•	You can still keep a separate backup strategy (e.g., one 9TB kept as periodic offline mirror).

⸻

🧩 Services & Workloads
	•	Kavita & Mylar3 live directly on the core server (Docker / native), reading/writing from comics/* datasets.
	•	Portainer runs on the core server and manages containers on:
	•	Core server itself
	•	Zima
	•	Hawkeye
	•	Others (via Portainer agents).
	•	NFS/SMB exports replace local mounts on The Beast:
	•	The Beast now sees network shares instead of USB disks.
	•	Optional: run Home Assistant on the core server (as a VM or container) so your home automation brain is in the same always-on appliance.

⸻

🧵 Role Changes Summary
	•	The Beast
	•	Becomes a pure workstation: editing, scripting, dev, maybe one-off video transcoding.
	•	No longer responsible for 70TB of spinning rust via USB.
	•	Core Server
	•	New “sun” of the storage solar system.
	•	Runs 24/7, low power, optimized for disks + network.
	•	Hosts Docker, NFS/SMB, monitoring, Mylar, Kavita, etc.
	•	Zima, Hawkeye, Hippy, Sweetpea
	•	Become lightweight nodes:
	•	Consumers of NFS/SMB shares.
	•	Optional Docker workloads for specific tasks.
	•	Backed up to backups/lab_nodes on the core server.

⸻

If you’d like, next step we can:
	•	Pick one concrete OS for the core (TrueNAS SCALE vs Unraid vs OMV) and draw a more detailed “final” diagram for that choice, or
	•	Draft a migration checklist: in what order to move which disks from USB → SATA, how to keep everything online while you transition.
