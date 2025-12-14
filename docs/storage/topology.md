```mermaid
graph TD
    BEAST["🖥️ The Beast (Workstation / Lab Hub)"]

    subgraph MB["Motherboard"]
        subgraph SATA["SATA Ports (x6)"]
            sda["sda – 4TB HDD"]
            sdb["sdb – 4TB HDD"]
            sdc["sdc – 4TB HDD (root member)"]
            sdd["sdd – 4TB HDD (root member)"]
            sata5["(unused / free SATA)"]
            sata6["(unused / free SATA)"]
        end

        subgraph NVME["M.2 NVMe Slots (x3)"]
            nvme0["nvme0n1 – 1TB (old root)"]
            nvme1["nvme1n1 – 1TB (old home)"]
            nvme2["(empty or reserved)"]
        end
    end

    BEAST --> MB

    %% USB topology
    subgraph USB["USB3 Storage"]
        subgraph DAS["DAS Enclosure (JMicron JMS551)"]
            sde["sde – 14TB HDD"]
            sdf["sdf – 14TB HDD"]
        end

        sdg["sdg – 7TB USB HDD (/mnt/data)"]
        sdh["sdh – 9TB USB HDD (/mnt/arcs)"]
        sdi["sdi – 9TB USB HDD (/mnt/pubs, /mnt/Marvel)"]
    end

    BEAST -->|single USB3 cable| DAS
    BEAST -->|USB3 hubs/ports| sdg
    BEAST -->|USB3 hubs/ports| sdh
    BEAST -->|USB3 hubs/ports| sdi
