
#import "@preview/arkheion:0.1.0": arkheion, arkheion-appendices
#import "@preview/equate:0.2.1": equate
#import "@preview/wrap-it:0.1.0": wrap-content
#show link: it => underline(text(fill: blue)[#it])
#set page(paper: "a4", margin: (left: 10mm, right: 10mm, top: 12mm, bottom: 15mm))
// #set par.line(numbering: n => text(size: 6pt)[#n])
// #set par.line(numbering: "1")
//-> will work in next release ("soon")
#show: arkheion.with(
  title: "Automating Data Integration and Archival for EEG Neuroimaging via LSLAutoBIDS",
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

Modern neuroscience research often relies on collecting complex, multimodal datasets, combining behavioral data, eye-tracking and neuroimaging (e.g. EEG) data. Such datasets are valuable for understanding cognitive processes but are often challenging to collect due to the resource-intensive nature of experiments and the logistical demands. They are often collected by trainees or research assistants with limited prior experience or training. To increase the robustness of data analysis pipelines, as well as encourage data sharing, we present a program to automate some parts of their workflow in terms of four aspects: data integration, data organization, data versioning and data archiving.​ Such an automated workflow promotes open science by design @national_academies_of_sciences_engineering_and_medicine_open_2018:

*Data Integration:* Collected data often comes from many sources. LabStreamingLayer (LSL) @kothe_lab_2024 has become a standard way to record multiple data streams and synchronize their time-series. In addition, other data sources need to be collected from devices that cannot send them actively  (e.g., experimental logging files, eye-tracking data).

*Data Organization:* To allow machines and humans to navigate such a diverse dataset, the Brain Imaging Data Structure (BIDS) @gorgolewski_brain_2016 standard provides a well-described framework, offering consistent directory structure, file naming conventions, and metadata descriptors for neuroimaging data. The recorded dataset can then be seamlessly integrated into analysis pipelines, promoting data sharing.

*Data Versioning:* The next aspect is to include datasets into version control. While much progress has been made in version control for analysis code, datasets are only rarely versioned by default. DataLad @halchenko_datalad_2021, which is based on git and git-annex, allowing for efficient versioning of not only code, but also binary files. Crucially, adding new subjects, annotations, or corrections will leave a trace, greatly improving transparency of the process and allowing decentralized data management @hanke_defense_2021.

*Data Archiving* The last step, which is often only done after the data has been fully analysed, is the long-term archiving. Immediately archiving the raw data has the benefit of frontloading (and externalising) the additional effort required to archive the data, thus it cannot be omitted or forgotten. Automating this is possible by linking the DataLad @halchenko_datalad_2021 datasets directly with a datasharing platform such as Dataverse, which will provide Digital Object Identifiers (DOI) and customizable access controls.


In our work, we addressed all four aspects in a single automated workflow. Our contributions are: (1) we discuss workflow to integrate community standards for data organization, automated archiving, and version control, with the potential to generalize across modalities and experimental paradigms, (2) we introduce `LSLAutoBIDS`, a Python package as an example implementation for such a workflow, using Lab Streaming Layer @kothe_lab_2024, converting to BIDS, versioning via Datalad @halchenko_datalad_2021, and archiving via Dataverse.

= Related Works
/*it becomes significantly more difficult to manipulate or selectively alter data post hoc, thereby reducing the risk of scientific misconduct and improving the credibility of the research process (Proof of correctness included here). - just not to forget the point */ 


/*idea : data standardization papers (BIDS and its extension papers) -> Datalad integration in most data management projects - Use of different type of database management (SQLite) - Some papers try to automate source to BIDS (BIDSCoin, mne-bids)- large scale projects reference and our integration to the workflow.*/

The pioneering work of Dobson et. al @dobson_presentations_2018 needs to be highlighted first here. They propose "ReproIn", a tool quite similar to ours, that converts DICOM data from an MR scanner to BIDS, and finally saves it in a DataLad repository. Compared to our implementation, "ReproIn" relies on a fMRI scanner, whereas we use LSL to integrate data, instead of `heudiconv` we use `mnelab`, `pylsl` and `mne-bids`. While "ReproIn" does not automatically link the DataLad repository to a dataverse, this additional step could be readily implemented to "ReproIn" as well.

A different example for a data management workflow, incorporating standardization and archiving, i.e, from raw data acquisition to organization/standardization to analysis, is presented in Stawiski et al., @stawiski_optimizing_2024. In this project, they collected heterogeneous raw data of more than 100 participants in two clinics, transformed them to BIDS, and use SQLite to manage the resulting dataset. Even though they do not discuss versioning and archiving, it is easily conceivable how these steps could be added to their workflow.

/*Over the years, numerous studies have been conducted in the domain of EEG, making it an important area of active research in cognitive neuroscience. */The aforementioned Brain Imaging Data Structure @gorgolewski_brain_2016, originally proposed for magnetic resonance imaging (MRI) is a community standard for data organization and sharing of brain data within research communities. This standard is designed using the FAIR (findability, accessibility, interoperability, and reusability) principles @wilkinson_fair_2016, contributing to efficient scientific data management and stewardship. Following the release of the BIDS standard, a lot of extensions concerning integration of BIDS with different neuroimaging techniques like magnetoencephalography (MEG) @niso_meg-bids_2018, intracranial electroencephalography (iEEG) @holdgraf_ieeg-bids_2019, electroencephalography (EEG) @pernet_eeg-bids_2019, Positron Emission Tomography (PET) @norgaard_pet-bids_2022, etc., were developed. Data sharing and reuse of these BIDS complaint datasets was eventually simplified using open source sharing platforms like OpenNeuro @markiewicz_openneuro_2021, which hosts more than 600 datasets in compliance with BIDS. 

Additionally, packages like `mne-bids` @appelhoff_mne-bids_2019 or `BIDSCoin` @zwiers_bidscoin_2022 are useful for converting any raw source data to BIDS-compliant datasets and finally validating the conversion using the BIDS validator @gorgolewski_brain_2016.  Extending these developments, @gorgolewski_bids_2017 proposed a cross-platform, containerized framework for standardized analysis of BIDS datasets across heterogeneous computing environments, including multi-tenant clusters. To make it more user-friendly for researchers, BIDSCoin @zwiers_bidscoin_2022 offers a graphical user interface, making it accessible even to those without programming experience, unlike `mne-bids`.

/* 
To add to this ease of data management, @covitz_curation_2022 adds another layer where users can validate BIDS standard, summarize BIDS metadata, etc, along with version control using Datalad @halchenko_datalad_2021. 
*/

Unlike software and code versioning, data versioning is only rarely practiced, given issues in practicality to version large binary files. Nevertheless, version control is an important aspect in data collection to ensure data traceability and an error-free workflow. DataLad @halchenko_datalad_2021, based on git-annex, nicely extends the capabilities of classical git versioning tools, to large, binary datasets. DataLad is actively used in hundreds of studies.




/*
In our workflow, we attempt to incorporate many of the currently available aspects for an efficient data management pipeline, which are currently incorporated in parts by the cited research, and automate the entire process of archiving our recorded heterogeneous data in a standardized BIDS format and depositing it in a Dataverse repository via version control using DataLad. The tool is easily extensible to other input modalities with minimal modifications.
*/
= LSLAutoBIDS
#figure(
  image("2025-05-20_lsl-flowchart.svg", width: 100%),
  caption: [Flowchart of LSLAutoBIDS. On the left, we start with some data that we record using LabStreamingLayer-tools and propretiory tools. Once several files have been generated, we use LSLAutoBIDS to integrate them (1), meaning collection and synchronisation. Next we (2) organize these data to the BIDS data format. Using DataLad, we (3) version them, and finally upload them to an open repository like DataVerse or OpenNeuro (not yet implemented).]
) <glacier>
`LSLAutoBIDS` is an open-source Python package developed and actively used by the Computational Cognitive Science Lab at the University of Stuttgart. It offers a modular and reproducible workflow tailored for studies using Lab Streaming Layer (LSL) based data acquisition, specifically targeting the integration of electroencephalography (EEG) and eye-tracking modalities. 

In this setup, participant-level EEG data, but potentially also other LSL streams (eyetracking, motion tracking) is recorded using the Lab Streaming Layer (LSL) protocol, which allows for sub-millisecond time-synchronization of heterogeneously sampled streams. Project metadata like authors, license, experimental description, but also dataverse details are recorded in one central configuration-toml file, which is then used to retrieve these project-specific metadata during the conversion process. The recorded raw data streams are then converted into the Brain Imaging Data Structure (BIDS) @gorgolewski_brain_2016 standard using the `mnelab`, `pylsl` `mne` and `mne_bids` @appelhoff_mne-bids_2019 package. Once converted, the BIDS-compliant dataset is automatically deposited into a Dataverse repository, along with the experiment stimulus files and the raw data streams.

In addition to LSL-based EEG data acquisition, `LSLAutoBIDS` supports the incorporation of non-LSL data. For example, in our use-case, eye-tracking data are collected using the EyeLink 1000 Plus eye tracker simultaneously with EEG data collection, which produces proprietary Eyelink data format (EDF) files which cannot easily be streamed via LSL. Other examples are an electronic labnotebook record, log-files of the experiment, and a compressed archive of the experimental code used for any each subject individually. `LSLAutoBIDS` accommodates these files as a secondary data modality currently implemented via a netshare drive, and is able to organize them within the appropriate BIDS subdirectories to archive them alongside EEG data.

Version control is integrated into the pipeline using DataLad @halchenko_datalad_2021, enabling precise tracking of all data and metadata changes across the research lifecycle, including modification or re-transformation of the individual files.

After each recording session, the dataset is then uploaded to a Dataverse repository, where it is persistently archived with the specified metadata. After data collection is finished, the dataset can there be versioned for release, and publicly shared with an appropriate data sharing agreement.

The architecture of `LSLAutoBIDS` is deliberately designed to be extensible. Additional files, such as behavioral data, audio recordings, or physiological signals, can be integrated by extending configuration templates and adding corresponding processing steps. This generalizability makes `LSLAutoBIDS` not just a tool for EEG and eye-tracking studies, but a proof of concept for broader multimodal data workflows in cognitive neuroscience.

The LSLAutoBIDS package is continuously developed and freely available: #link("https://github.com/s-ccs/LSLAutoBIDS")

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
