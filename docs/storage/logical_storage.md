```mermaid
graph TD

    %% Btrfs RAID1: fearless (14TB mirror over USB DAS)
    subgraph FEARLESS_FS["Btrfs FS: 'fearless' (≈14TB RAID1)"]
        fearless["Label: fearless<br/>Btrfs RAID1 (data+metadata)"]
    end

    sde["/dev/sde – 14TB (DAS bay 1)"]
    sdf["/dev/sdf – 14TB (DAS bay 2)"]

    sde --> fearless
    sdf --> fearless

    fearless --> mnt_fearless["/mnt/fearless"]
    fearless --> mnt_dc["/mnt/DC"]
    fearless --> mnt_longbox["/mnt/longbox"]
    fearless --> mnt_shortbox["/mnt/shortbox"]

    %% Btrfs RAID1: root/home pool
    subgraph ROOT_FS["Btrfs FS: system pool (root + /home)"]
        rootfs["Btrfs RAID1<br/>/ + /home"]
    end

    sdc2["/dev/sdc2 – 4TB (system)"]
    sdd2["/dev/sdd2 – 4TB (system mirror)"]

    sdc2 --> rootfs
    sdd2 --> rootfs

    rootfs --> slash["/ (root)"]
    rootfs --> home["/home"]

    %% Btrfs RAID1: grackle
    subgraph GRACKLE_FS["Btrfs FS: 'grackle' (≈4TB RAID1)"]
        grackle["Label: grackle<br/>Btrfs RAID1"]
    end

    sda_dev["/dev/sda – 4TB"]
    sdb_dev["/dev/sdb – 4TB"]

    sda_dev --> grackle
    sdb_dev --> grackle

    grackle --> mnt_grackle["/mnt/grackle"]

    %% Single-disk ext4 volumes (USB drives)
    sdg_dev["/dev/sdg1 – 7TB ext4"]
    sdh_dev["/dev/sdh1 – 9TB ext4"]
    sdi_dev["/dev/sdi1 – 9TB ext4"]

    sdg_dev --> mnt_data["/mnt/data"]
    sdh_dev --> mnt_arcs["/mnt/arcs"]
    sdi_dev --> mnt_pubs["/mnt/pubs"]
    sdi_dev --> mnt_marvel["/mnt/Marvel"]

    %% NVMe legacy mounts
    nvme0p2["nvme0n1p2 – ext4"]
    nvme1p1["nvme1n1p1 – ext4"]

    nvme0p2 --> oldroot["/media/oldboot_root"]
    nvme1p1 --> oldhome["/home/rmleonard_old"]
