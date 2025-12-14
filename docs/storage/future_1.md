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
