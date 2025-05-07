
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
    
The domain of cognitive neuroscience necessitates rigorous data collection, organization, long-term archiving, and traceable version control. This process presents significant challenges due to heterogeneous data formats and the lack of standardized, domain-specific procedures for systematic data archiving and version management. We present `LSLAutoBIDS`, a prototype framework that demonstrates how existing standards such as the Brain Imaging Data Structure (BIDS), DataLad, and Dataverse can be integrated to support automated, reproducible, and transparent data lifecycles. `LSLAutoBIDS` specifically targets Electroencephalogram (EEG) data recorded via Lab Streaming Layer (LSL), converting these streams into BIDS-compliant datasets, archiving them automatically to a Dataverse instance, and maintaining full version control. Designed as both a reference implementation and a practical tool, `LSLAutoBIDS` supports lab automation and serves as a template for developing similar domain-specific solutions across experimental neuroscience and beyond.
  ],
  keywords: ("Brain Imaging Data Structure", "version control", "Electroencephalogram"),
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

The introduction is structured as follows :
- Intro paragraph
- Why are data-organisation important? - 	-> link to BIDSCoiner
- Why is archiving data important?
- Why is versioning of datasets important?
- Our contributions


Modern neuroscience research increasingly relies on the acquisition of complex, multimodal datasets, such as electroencephalogram (EEG), behavior, and/or eye-tracking recordings. These datasets are valuable for understanding cognitive processes but are often challenging to collect due to the resource-intensive nature of experiments and the logistical demands of managing large participant cohorts. To increase the robustness of data analysis pipelines, as well as encourage data sharing we focus on automating three aspects here: standadized data organization, automated data archiving, and robust version control.​

The diversity of data formats and acquisition modalities in neuroscience necessitates a unified approach to data standardization and structuring. The Brain Imaging Data Structure (BIDS) @gorgolewski_brain_2016 standard has emerged as a pivotal framework in this context, prescribing a consistent directory structure, file naming conventions, and metadata descriptors for neuroimaging data. Such standards also ensures that the data is both machine-readable and human-interpretable, facilitating seamless integration into analysis pipelines and promoting data sharing.​ Tools like BIDSCoin @zwiers_bidscoin_2022 have been developed to streamline the conversion of various raw neuroimaging data into BIDS-compliant formats.
/*BIDScoin provides a graphical user interface which allows researchers to interactively refine these mappings and also eases the complexity of performing such complex analysis pipeline.*/

Beyond structuring, the long-term archiving of research data is important for enabling reanalysis, supporting future meta-studies, and ensuring transparency and accountability in empirical claims. Manual data archiving is prone to inconsistencies and omissions, which can undermine the reproducibility of findings. Automating this process as part of the experimental workflow reduces the potential for human error and ensures that data is systematically deposited into secure repositories. Platforms such as Dataverse support this model by enabling dataset registration with persistent digital object identifiers (DOIs) and customizable access controls, thus preserving data in a format that is both accessible and citable.

Our third aspect is to expand version control to the data as well @halchenko_datalad_2021. This helps in maintaining data integrity over time, and allows to update a dataset with new cohorts, annotations, or corrections. 


In our lab, we strive to address all three of these aspects into one automated workflow. Our contributions are: (1) we propose a modular and reproducible workflow for cognitive neuroscience research that integrates community standards for data organization, automated archiving, and robust version control, with the potential to generalize across modalities and experimental paradigms, (2) we introduce `LSLAutoBIDS`, a Python package implementing a pipeline from multi-modal neuroimaging data recorded via Lab Streaming Layer (Didn't find the correct citation), to BIDS conversion, dataset versioning via datalad  @halchenko_datalad_2021, and archiving via dataverse. 

= Related Works
Is this section required? - I think if there is related work, we should absolutely cite it. maybe we discover that someone already did all of this (I know that a similar, but more limited system is in place at the donders, where bidscoiner was developed as well

/*it becomes significantly more difficult to manipulate or selectively alter data post hoc, thereby reducing the risk of scientific misconduct and improving the credibility of the research process (Proof of correctness included here). */ 


idea : data standardization papers (BIDS and its extension papers) -> Datalad integration in most data management projects - Use of different type of database management (SQLite) - Some papers try to automate source to BIDS (BIDSCoin, mne-bids)- large scale projects reference and our integration to the workflow.

Over the years, numerous studies have been conducted in the domain of electroencephalography (EEG), making it an important area of active research in cognitive neuroscience. The Brain Imaging Data Structure @gorgolewski_brain_2016 orginally proposed for magnetic resonance imaging (MRI) is a community standard for data organization and sharing of brain data within research communities. This standard is designed using the FAIR (findability, accessibility, interoperability, and reusability) principles @wilkinson_fair_2016 contributing to efficient scientific data management and stewardship. Following the release of BIDS standard a lot of extensions concerning different medical imaging and neuroimaging techniques like magnetoencephalography (MEG) @niso_meg-bids_2018 , intracranial electroencephalography (iEEG) @holdgraf_ieeg-bids_2019, electroencephalography (EEG) @pernet_eeg-bids_2019, Positron Emission Tomography (PET) @norgaard_pet-bids_2022, etc are developed. Data sharing and reuse was eventually simplified using open source sharing platforms like OpenNeuro @markiewicz_openneuro_2021 which hosts more than 600 datasets in compliance with BIDS. Packages like `mne-bids` @appelhoff_mne-bids_2019 and BIDSCoin @zwiers_bidscoin_2022 helps to convert our raw EEG data to BIDS compliant datasets. To facilitate the analysis of these converted BIDS data in cross platform setups and multi tenant clusters @gorgolewski_bids_2017 developed a cross platform containerized framework to ease the usage of BIDS data analysis pipelines.


= LSLAutoBIDS
`LSLAutoBIDS` is an open-source Python package developed and actively used by the Computational Cognitive Science Lab at the University of Stuttgart. It offers a modular and reproducible workflow tailored for studies using Lab Streaming Layer (LSL) based data acquisition, specifically targeting the integration of electroencephalography (EEG) and eye-tracking modalities. 

In this setup participant level EEG data is recorded using the Lab Streaming Layer (LSL) protocol, which provides time-synchronized streams from the EEG electrodes. The recorded raw data streams are then converted into the Brain Imaging Data Structure (BIDS) @gorgolewski_brain_2016 standard using the `mne_bids` @appelhoff_mne-bids_2019 package. (some more infomation about BIDS to be included ?). Once converted, the BIDS-compliant dataset is automatically deposited into a Dataverse repository, along with the experiment stimulus files and the raw data streams.

In addition to LSL based EEG data acquisition, `LSLAutoBIDS` supports the incorporation of auxiliary modalities. For example, in current use, eye-tracking data are collected using the EyeLink 1000 Plus eye tracker simultaneously with EEG data collection, which produces proprietary Eyelink data format (EDF) files independently of the LSL stream. `LSLAutoBIDS` accommodates these files as a secondary data modality by organizing them within the appropriate BIDS subdirectories and archiving them alongside EEG data. 

The full dataset, comprising both EEG and eye-tracking components, is then automatically uploaded to a Dataverse repository, where it is persistently archived with assigned metadata, version history, and access controls. Version control is integrated into the pipeline using DataLad @halchenko_datalad_2021, enabling precise tracking of all data and metadata changes across the research lifecycle. Built on Git and Git-annex, DataLad @halchenko_datalad_2021 supports versioning of large datasets, allowing researchers to create reproducible snapshots, inspect histories of modifications, and synchronize dataset states across machines or collaborators.

The architecture of `LSLAutoBIDS` is deliberately designed to be extensible. Additional files, such as behavioral data, audio recordings, or physiological signals, can be integrated by extending configuration templates and adding corresponding processing steps. This generalizability makes `LSLAutoBIDS` not just a tool for EEG and eye-tracking studies, but a proof of concept for broader multimodal data workflows in cognitive neuroscience.


The LSLAutoBIDS package is available in github : #link("https://github.com/s-ccs/LSLAutoBIDS")
= Funding

Funded by Deutsche Forschungsgemeinschaft (DFG, German Research Foundations) in the Emmy Noether Programme - Project-ID 538578433. The authors further thank the International Max Planck Research School for Intelligent Systems (IMPRS-IS) for supporting Judith Schepers.

#set par(justify: true, first-line-indent: 0pt);


// send behinger an email with your zotero to get access to the group
#bibliography(title:"Bibliography", style:"american-psychological-association", "zotero.bib")


= Rough Notes for references and Citations

1. EEG-BIDS : BIDS extension for EEG. BIDS intially started as an MRI standardization. "BIDS primarily addresses the heterogeneity of data organization by following the FAIR principles3 of findability, accessibility, interoperability, and reusability." . "BIDS addresses findability and reusability by providing rich metadata in dedicated sidecar files and interoperability by using existing standard data formats. Accessibility is not directly addressed by BIDS, but by repositories that build on BIDS, such as OpenNeuro". 
2. ChineseEEG - Study of 10 participants where they used EEG and eye tracking modalities to collect EEG as well as ET data while partcipants read Chinese novels for 13 hours - https://www.nature.com/articles/s41597-024-03398-7
3. https://github.com/OpenNeuroDatasets/ Collection of BIDS compliant datasets (mainly MRI)
4. The evolution and future prospects of BIDS : @poldrack_past_2024
5. Data Organization and Sharing based on compliance to the FAIR (Findable, Accessible, Interoperable, Reusable) principles.@wilkinson_fair_2016
6. ExDir : Similar data organization standard like BIDS : https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2018.00016/full
7. This is one study with 100+ participants and very recent from 2024, where the paper focusses on data management where they use multimodal clinical data and converts it into standardized format (one of them is BIDS) and then store it in SQLite database. https://www.semanticscholar.org/paper/Optimizing-neuroscience-data-management-by-REDCap%2C-Stawiski-Bucciarelli/9992e8d281c7de6142d92c1994a2ea4a6ff9d220