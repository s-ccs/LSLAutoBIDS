
#import "@preview/arkheion:0.1.0": arkheion, arkheion-appendices
#import "@preview/equate:0.2.1": equate
#import "@preview/wrap-it:0.1.0": wrap-content
#show link: it => underline(text(fill: blue)[#it])
#set page(paper: "a4", margin: (left: 10mm, right: 10mm, top: 12mm, bottom: 15mm))
// #set par.line(numbering: n => text(size: 6pt)[#n])
// #set par.line(numbering: "1")
//-> will work in next release ("soon")
#show: arkheion.with(
  title: "Automated Data Structuring and Archival for Cognitive Experiments via LSLAutoBIDS",
  authors: (

    (name: "Manpa Barman",
    email: "st184660@stud.uni-stuttgart.de", 
    affiliation: "University of Stuttgart", 
    orcid: "0009-0005-6211-5289"),


    (name: "Benedikt Ehinger", 
    email: "benedikt.ehinger@vis.uni-stuttgart.de", 
    affiliation: "University of Stuttgart - SimTech", 
    orcid: "0000-0002-6276-3332"), 
  ),
  // Insert your abstract after the colon, wrapped in brackets.
  // Example: `abstract: [This is my abstract...]`
  abstract: [
    
Cognitive neuroscience routinely collect large datasets, yet data integration, organization, version control and archiving is rarely automatized. Here, we present such a workflow, offering open science by design, with an  implementation in the python based `LSLAutoBIDS` open-source package. We first describe our exemplary workflow based on LabStreamingLayer (to integrate), BIDS (to transform), DataLad (to version) and Dataverse (to archive), before discussing the place such tools can have in future data collection efforts.
  ],
  keywords: ("BIDS", "EEG","LSL", "Lab Streaming Layer", "Dataverse", "Datalad", "archiving", "data collection"),
  date: "30th April, 2024",
) 

// set spellcheck language
#set text(lang: "en", region: "US")

// figure caption alighment
#show figure.caption: set align(center)

//#elements.float(align: bottom, [\*Corresponding author]) 
#set figure(gap: 0.5em) /* Gap between figure and caption */
#show figure: set block(inset: (top: 0.5em, bottom: 1.5em)) /* Gap between top/ bottom of figure and body text */

//#show: equate.with(breakable: false, sub-numbering: true) /* Needed for multi line equations */
#set math.equation(numbering: "(1.1)")

#set heading(numbering: "1." )

#pagebreak()
= Introduction

Modern neuroscience research often relies on collecting complex, multimodal datasets, combining behavioral data, eye-tracking and neuroimaging (e.g. EEG). Such datasets are valuable for understanding cognitive processes but are often challenging to collect due to the resource-intensive nature of experiments and the logistical demands. They are often collected by trainees or research assistants with limited prior experience or training. To increase the robustness of data analysis pipelines, as well as encourage data sharing, we present a program to automate some parts of their workflow in terms of four aspects: data integration, data transformation, version control and data archiving.​ Such an automated pathway offers open science by design @national_academies_of_sciences_engineering_and_medicine_open_2018:

*Data integration:* Collected data often comes from many sources. LabStreamingLayer has become a standard way to record multiple data streams and synchronize their time-series. In addition, other data sources need to be collected from other devices that cannot actively send it (e.g. experimental log-files, eye-tracking data).

*Data Transformation:* To allow machines and humans to navigate such a diverse dataset, the Brain Imaging Data Structure (BIDS) @gorgolewski_brain_2016 standard provides a well described framework, offering consistent directory structure, file naming conventions, and metadata descriptors for neuroimaging data. The resulting dataset can be seamlessly integrated into analysis pipelines and promotes data sharing.​

*Data Versioning:* the next aspect is to include datasets into version control. While much progress has been made for version control for analysis code, datasets are only rarely versioned by default. In our workflow we make use of DataLad @halchenko_datalad_2021 which is based on git-annex, allowing for efficient versioning of not only code, but also binary files. Crucially, adding new subjects, annotations, or corrections will leave a trace, greatly improving the transparency of the process. 

*Data Archiving* the last step, which often is only done after the data were fully analysed, is the long-term archiving. Here we propose to immediately archive the raw data. This has the benefit that you are frontloading (and externalising) the additional work to archive the data, thus it cannot be ommitted or forgotten. Automating this is possible by linking the DataLad dataset directly with a datasharing platform such as Dataverse, which will provide DOIs and customizable access controls.


In our lab, we addressed all four aspects in a single automated workflow. Our contributions are: (1) we discuss workflow to integrate community standards for data organization, automated archiving, and version control, with the potential to generalize across modalities and experimental paradigms, (2) we introduce `LSLAutoBIDS`, a Python package as an example implementation for such a workflow, using Lab Streaming Layer @kothe_lab_2024, converting to BIDS, versioning via datalad @halchenko_datalad_2021, and archiving via dataverse.

= Related Works
/*it becomes significantly more difficult to manipulate or selectively alter data post hoc, thereby reducing the risk of scientific misconduct and improving the credibility of the research process (Proof of correctness included here). - just not to forget the point */ 


/*idea : data standardization papers (BIDS and its extension papers) -> Datalad integration in most data management projects - Use of different type of database management (SQLite) - Some papers try to automate source to BIDS (BIDSCoin, mne-bids)- large scale projects reference and our integration to the workflow.*/
The pioneering work of Dobson et. al @dobson_presentations_2018 needs to be highlighted first here. They propose "ReproIn", a tool quite similar to ours, that converts DICOM data from an MR scanner to BIDS, and finally saves it in a DataLad repository. Compared to our implementation, "ReproIn" relies on a fMRI scanner, whereas we use LSL to integrate data, instead of `heudiconv` we use `mnelab`, `pylsl` and `mne-bids`. While "ReproIn" does not automatically link the DataLad repository to a dataverse, this additional step could be readily implemented to "ReproIn" as well.

/*Over the years, numerous studies have been conducted in the domain of EEG, making it an important area of active research in cognitive neuroscience. */The Brain Imaging Data Structure @gorgolewski_brain_2016 originally proposed for magnetic resonance imaging (MRI) is a community standard for data organization and sharing of brain data within research communities. This standard is designed using the FAIR (findability, accessibility, interoperability, and reusability) principles @wilkinson_fair_2016, contributing to efficient scientific data management and stewardship. Following the release of the BIDS standard a lot of extensions concerning different medical imaging and neuroimaging techniques like magnetoencephalography (MEG) @niso_meg-bids_2018, intracranial electroencephalography (iEEG) @holdgraf_ieeg-bids_2019, electroencephalography (EEG) @pernet_eeg-bids_2019, Positron Emission Tomography (PET) @norgaard_pet-bids_2022, etc were developed. Data sharing and reuse of datasets was eventually simplified using open source sharing platforms like OpenNeuro @markiewicz_openneuro_2021 which hosts more than 600 datasets in compliance with BIDS. 

Concerning the conversion to BIDS, packages like `mne-bids` @appelhoff_mne-bids_2019 or `BIDSCoin` @zwiers_bidscoin_2022 help to convert any raw source data to BIDS compliant datasets and finally validate the conversion using the BIDS validator @gorgolewski_brain_2016. To enhance user-friendliness for researchers, BIDSCoin @zwiers_bidscoin_2022 offers a graphical user interface, making it accessible even to those without programming experience, unlike `mne-bids`. Extending these developments, @gorgolewski_bids_2017 proposed a cross-platform, containerized framework designed to facilitate the standardized analysis of BIDS datasets across heterogeneous computing environments, including multi-tenant clusters.

To add to this ease of data management, @covitz_curation_2022 adds another layer where users can validate BIDS standard, summarize BIDS metadata, etc, along with version control using Datalad @halchenko_datalad_2021.

Version control is an important aspect in data collection to ensure data traceability and an error-free workflow. Studies with a large number of participants like the _Narratives collection_ @nastase_narratives_2021, `highspeed` datasets @wittkuhn_dynamics_2021, used Datalad for versioning and organizing their datasets. Data management workflows, incorporating standardization and archiving, i.e, from raw data acquisition to organization/standardization to analysis, are dealt with by Stawiski et al., @stawiski_optimizing_2024. In this study, they exhibit a prototype of collecting heterogeneous raw data with more than 100 participants for a Deep Brain Simulation Research (DBS), including BIDS-compliant checks and database management using SQLite, and finally using Python-based libraries like Numpy for the analysis pipeline.

/*
In our workflow, we attempt to incorporate many of the currently available aspects for an efficient data management pipeline, which are currently incorporated in parts by the cited research, and automate the entire process of archiving our recorded heterogeneous data in a standardized BIDS format and depositing it in a Dataverse repository via version control using DataLad. The tool is easily extensible to other input modalities with minimal modifications.
*/
= LSLAutoBIDS
#figure(
  image("2025-05-20_lsl-flowchart.svg", width: 100%),
  caption: [Flowchart of LSLAutoBIDS. On the left, we start with some data that we record using LabStreamingLayer-tools and propretiory tools. Once several files have been generated, we use LSLAutoBIDS to integrate them (1), meaning collection and synchronisation. Next we (2) transform these data to the BIDS data format. Using DataLad, we (3) version them, and finally upload them to an open repository like DataVerse or OpenNeuro (not yet implemented).],
) <glacier>
`LSLAutoBIDS` is an open-source Python package developed and actively used by the Computational Cognitive Science Lab at the University of Stuttgart. It offers a modular and reproducible workflow tailored for studies using Lab Streaming Layer (LSL) based data acquisition, specifically targeting the integration of electroencephalography (EEG) and eye-tracking modalities. 

In this setup, participant-level EEG data is recorded using the Lab Streaming Layer (LSL) protocol, which provides time-synchronized streams from the EEG electrodes. (_Can we write a bit more about the electrode setup and LSL?_) The recorded raw data streams are then converted into the Brain Imaging Data Structure (BIDS) @gorgolewski_brain_2016 standard using the `mnelab`, `pylsl` `mne` and `mne_bids` @appelhoff_mne-bids_2019 package. (some more infomation about BIDS to be included ?). Once converted, the BIDS-compliant dataset is automatically deposited into a Dataverse repository, along with the experiment stimulus files and the raw data streams.

In addition to LSL based EEG data acquisition, `LSLAutoBIDS` supports the incorporation of auxiliary modalities. For example, in current use, eye-tracking data are collected using the EyeLink 1000 Plus eye tracker simultaneously with EEG data collection, which produces proprietary Eyelink data format (EDF) files which cannot online be streamed via LSL. `LSLAutoBIDS` accommodates these files as a secondary data modality connected via a netshare drive, and organizes them within the appropriate BIDS subdirectories to archive them alongside EEG data. 

The full dataset, comprising both EEG and eye-tracking components, is then automatically uploaded to a Dataverse repository, where it is persistently archived with assigned metadata, version history, and access controls. Version control is integrated into the pipeline using DataLad @halchenko_datalad_2021, enabling precise tracking of all data and metadata changes across the research lifecycle. Built on Git and Git-annex, DataLad @halchenko_datalad_2021 supports versioning of arbitrarily large datasets, allowing researchers to create reproducible snapshots, inspect histories of modifications, and synchronize dataset states across machines or collaborators.

The architecture of `LSLAutoBIDS` is deliberately designed to be extensible. Additional files, such as behavioral data, audio recordings, or physiological signals, can be integrated by extending configuration templates and adding corresponding processing steps. This generalizability makes `LSLAutoBIDS` not just a tool for EEG and eye-tracking studies, but a proof of concept for broader multimodal data workflows in cognitive neuroscience.


The LSLAutoBIDS package is available in github : #link("https://github.com/s-ccs/LSLAutoBIDS")

= Future Work

/* 
Write this out:
1. Modularizing LSLAutoBIDS to allow for easy addition of custom modules
2. The tradeoff of flexibility in e.g. the integration step vs. a "set-and-forget" configuration
*/
= Funding

Funded by Deutsche Forschungsgemeinschaft (DFG, German Research Foundations) in the Emmy Noether Programme - Project-ID 538578433. 

#set par(justify: true, first-line-indent: 0pt);


// send behinger an email with your zotero to get access to the group
#bibliography(title:"Bibliography", style:"american-psychological-association", "zotero.bib")


= Rough Notes for references and Citations

1. EEG-BIDS : BIDS extension for EEG. BIDS intially started as an MRI standardization. "BIDS primarily addresses the heterogeneity of data organization by following the FAIR principles3 of findability, accessibility, interoperability, and reusability." . "BIDS addresses findability and reusability by providing rich metadata in dedicated sidecar files and interoperability by using existing standard data formats. Accessibility is not directly addressed by BIDS, but by repositories that build on BIDS, such as OpenNeuro". 
2. ChineseEEG - Study of 10 participants where they used EEG and eye tracking modalities to collect EEG as well as ET data while partcipants read Chinese novels for 13 hours - https://www.nature.com/articles/s41597-024-03398-7
3. https://github.com/OpenNeuroDatasets/ Collection of BIDS compliant datasets (mainly MRI)
4. The evolution and future prospects of BIDS : @poldrack_past_2024
6. ExDir : Similar data organization standard like BIDS : https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2018.00016/full
