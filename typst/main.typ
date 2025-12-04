
#import "@preview/arkheion:0.1.0": arkheion, arkheion-appendices
#import "@preview/equate:0.2.1": equate
#import "@preview/wrap-it:0.1.0": wrap-content
#show link: it => underline(text(fill: blue)[#it])
#set page(paper: "a4", margin: (left: 10mm, right: 10mm, top: 12mm, bottom: 15mm))
#set par.line(numbering: n => text(size: 6pt)[#n])
#set par.line(numbering: "1")

#let revManpa(body) = text(fill: blue)[#body]
#let revBene(body) = text(fill: red)[#body]
//-> will work in next release ("soon")



//#import "lapreprint.typ": template
/*
#show: template.with(
  title: "A beautiful preprint template"
)

*/
#show: arkheion.with(
  title: "Automating Data Integration and Publishing for Neuroimaging via LSLAutoBIDS",
  authors: (

    (name: "Manpa Barman",
    email: "st184660@stud.uni-stuttgart.de", 
    affiliation: "University of Stuttgart, Institute for Visualization and Interactive Systems", 
    orcid: "0009-0005-6211-5289"),

    (name: "Jan Range",
    email: "jan.range@simtech.uni-stuttgart.de", 
    affiliation: "University of Stuttgart,  Stuttgart Center for Simulation Science; Institute of Biochemistry", 
    orcid: "0000-0001-6478-1051"),

    (name: "Benedikt Ehinger", 
    email: "benedikt.ehinger@vis.uni-stuttgart.de", 
    affiliation: "University of Stuttgart, Institute for Visualization and Interactive Systems; Stuttgart Center for Simulation Science", 
    orcid: "0000-0002-6276-3332"), 
  ),
  // Insert your abstract after the colon, wrapped in brackets.
  // Example: `abstract: [This is my abstract...]`
  abstract: [
    
Cognitive neuroscience routinely collect large datasets, yet data integration, curation, version control, and publishing is rarely automated. Here, we present such a workflow, offering open science by design, with an  implementation in the python based `LSLAutoBIDS` open-source package. We first describe our exemplary workflow based on LabStreamingLayer (to integrate), BIDS (to transform), DataLad (to version), and Dataverse (to publish), before discussing the place such tools can have in future data collection efforts.
  ],
  keywords: ("BIDS", "EEG", "Lab Streaming Layer", "Dataverse", "Datalad", "data collection", "datasets", "open science", "data standards"),
  date: "31th May, 2025",
) 

// set spellcheck language
#set text(lang: "en", region: "US")

// figure caption alignment
#show figure.caption: set align(center)

//#elements.float(align: bottom, [\*Corresponding author]) 
#set figure(gap: 0.5em) /* Gap between figure and caption */
#show figure: set block(inset: (top: 0.5em, bottom: 1.5em)) /* Gap between top/ bottom of figure and body text */

//#show: equate.with(breakable: false, sub-numbering: true) /* Needed for multi line equations */
#set math.equation(numbering: "(1.1)")

#set heading(numbering: "1." )

#pagebreak()
= Introduction

Modern neuroscience research often relies on collecting complex, multimodal datasets, for example, combining behavioural, eye-tracking, and neuroimaging (e.g., EEG) data. Such datasets are valuable for understanding cognitive processes, but are often challenging to collect due to the resource-intensive nature of experiments and the logistical demands. They are often collected by trainees or research assistants with limited prior experience or training. And even to more experienced data collectors, the following examples of what can go wrong will sound very familiar: 1) the same participant ID was used twice in a row, and data was irreversibly overwritten. 2) While running a study, the experiment was modified to fix a bug, but it was not documented after which subject it was fixed - later it remained unclear whether early subjects' data were retrogradely fixed or not. 3) A master's student left the lab without documenting their last dataset, leaving a mess of various files on various computers. 4) To move files from the various recording computers to their analysis system, every lab user seems to have their own idiosyncratic workflow, from USB sticks to WiFi hotspots. In this paper, we show that these issues can be prevented while at the same time saving time and training effort.

To increase the robustness of data recording pipelines, as well as to encourage data sharing, we present an approach to automate parts of this workflow. The automation we propose can be understood under the umbrella of open science by design@national_academies_of_sciences_engineering_and_medicine_open_2018. The central idea is to change infrastructure and workflows in a way that they are open from the point of creation, making "open science a by-product and not an afterthought"@national_academies_of_sciences_engineering_and_medicine_open_2018. In our case, the new data is curated and inserted into an existing dataset, versioned, and (privately) archived in a remote repository immediately after the recording. Additionally, many open data check boxes are also immediately marked without additional effort by the experimenter.

Our proposed workflow automates four main aspects of such data recording pipelines: data integration, data  curation, data versioning, and data publishing. ​

*Data Integration:* Collected data often comes from many sources. LabStreamingLayer (LSL) @kothe_lab_2024 has become a standard way to record multiple data streams and synchronize their time series. In addition, other data sources need to be collected from devices that cannot send them via LSL (e.g., experimental logging files, proprietary eye-tracking data).

*Data Curation:* To allow machines and humans to navigate such a diverse data collection, we want to structure them. The Brain Imaging Data Structure (BIDS) @gorgolewski_brain_2016 standard provides a well-described data curation environment, offering consistent directory structure, file naming conventions, and metadata descriptors for neuroimaging data. Once data is structured in BIDS format, the dataset can be seamlessly integrated into BIDS-compliant analysis pipelines.

*Data Versioning:* The next aspect is to include datasets into version control. While much progress has been made in version control for analysis code, datasets are only rarely versioned by default. DataLad @halchenko_datalad_2021 combines git and git-annex, allowing for efficient versioning of not only code, but also binary files. Crucially, adding new subjects, annotations, or corrections will leave a version trace, making the data collection robust to accidentally deleting or overwriting data and improving transparency of data provenance @hanke_defense_2021.

*Data Publishing:* Our last step, which traditionally is often only taken after the data has been fully analyzed, is the long-term archiving and (access-restricted) publishing. Immediately publishing the raw data has the benefit of frontloading (and externalizing) the additional effort required to publish the data. Automating this is made possible by linking the versioned DataLad @halchenko_datalad_2021 datasets directly with FAIR-enabling @wilkinson_fair_2016 data repositories such as Dataverse @crosas_dataverse_2011, which will provide Digital Object Identifiers (DOI), customizable access controls, archival service, and further automatic versioning.

In our work, we addressed all four aspects in a single automated workflow. Our contributions are: (1) we discuss workflow to integrate community standards for data curation, automated publishing, and version control, with the potential to generalize across modalities and experimental paradigms, (2) we introduce `LSLAutoBIDS`, a Python package as an example implementation for such a workflow, using Lab Streaming Layer @kothe_lab_2024, converting to BIDS, versioning via Datalad @halchenko_datalad_2021, and publishing via Dataverse.

= Related Works
/*it becomes significantly more difficult to manipulate or selectively alter data post hoc, thereby reducing the risk of scientific misconduct and improving the credibility of the research process (Proof of correctness included here). - just not to forget the point */ 


/*idea : data standardization papers (BIDS and its extension papers) -> Datalad integration in most data management projects - Use of different type of database management (SQLite) - Some papers try to automate source to BIDS (BIDSCoin, mne-bids)- large scale projects reference and our integration to the workflow.*/

The pioneering work of Dobson et al. @dobson_presentations_2018 should be highlighted: They present "ReproIn", a software package quite similar to ours, which converts DICOM data from an MR scanner to BIDS, and finally saves it in a DataLad repository. Compared to our implementation, "ReproIn" is optimized to work with different MR scanners, whereas we use LSL to integrate time-series data more directly. Instead of `heudiconv`, we use `mnelab`, `pylsl`, and `mne-bids` for the data curation stage. While "ReproIn" does not automatically link the DataLad repository to a Dataverse, this additional step could be readily implemented for "ReproIn" as well.

Another pioneering approach is taken at the Donders Institute for Brain and Cognition @noauthor_rdm_nodate. There, all fMRI and MEG data are automatically archived in a data acquisition collection (DAC). Other data needs to be added manually to the DAC. While the DAC is centralized, it is typically only used internally, and later, a data sharing collection (DSC) is created, which can be publicly shared. 


A different example for a data curation workflow, incorporating standardization and publishing, i.e, from raw data acquisition over standardization to analysis, is presented in Stawiski et al., @stawiski_optimizing_2024. In this project, they collected heterogeneous raw data of more than 100 participants in two clinics, transformed them to BIDS, and used SQLite to manage the resulting dataset. Even though they do not discuss versioning and publishing, it is easily conceivable how these steps could be added to their workflow.

The previously introduced *Brain Imaging Data Structure* @gorgolewski_brain_2016, originally proposed for magnetic resonance imaging (MRI), is a community standard for data  curation and sharing of brain data within research communities. This standard is designed using the FAIR (findability, accessibility, interoperability, and reusability) principles @wilkinson_fair_2016, contributing to efficient scientific data curation and stewardship. Following the release of the BIDS standard, numerous extensions were developed, concerning integration of BIDS with different neuroimaging techniques like magnetoencephalography (MEG) @niso_meg-bids_2018, intracranial electroencephalography (iEEG) @holdgraf_ieeg-bids_2019, electroencephalography (EEG) @pernet_eeg-bids_2019, Positron Emission Tomography (PET) @norgaard_pet-bids_2022, and others. Data sharing and reuse of these BIDS-complaint datasets is even further simplified using open-source sharing platforms, for instance, OpenNeuro @markiewicz_openneuro_2021, which currently hosts more than 600 datasets in compliance with BIDS. 

To *convert datasets* to be BIDS compliant, packages like `mne-bids` @appelhoff_mne-bids_2019, @yorguin-jose_sovabids_2025 or `BIDSCoin` @zwiers_bidscoin_2022 (using the sova2coin plugin) are essential to move and convert source data to BIDS-compliant datasets, and subsequently,  the BIDS validator @gorgolewski_brain_2016 can be used to validate the data collection.  To make the data conversion even more user-friendly for researchers, BIDSCoin @zwiers_bidscoin_2022 offers a graphical user interface, making it accessible even to those without programming experience. As far as we know, there is no dedicated LSL-to-BIDS converter available.

Unlike software and code versioning, *data versioning* is more rarely practiced, given issues in practicality to version large binary files. Nevertheless, version control is an important aspect in data collection to ensure data traceability and an error-free workflow. DataLad @halchenko_datalad_2021, based on git-annex, nicely extends the capabilities of classical git versioning tools to large, binary datasets. DataLad is actively used in hundreds of studies and underlies all datasets on OpenNeuro.



/*
In our workflow, we attempt to incorporate many of the currently available aspects for an efficient data management pipeline, which are currently incorporated in parts by the cited research, and automate the entire process of archiving our recorded heterogeneous data in a standardized BIDS format and depositing it in a Dataverse repository via version control using DataLad. The tool is easily extensible to other input modalities with minimal modifications.
*/
= LSLAutoBIDS
#figure(
  image("2025-09-12_lsl-flowchart.svg", width: 100%),
  caption: [Flowchart of LSLAutoBIDS. We start with different data streams recorded using LabStreamingLayer and as other proprietary file formats. (1) We use LSLAutoBIDS to integrate data that is collected across different computers and synchronise the data streams temporally. (2) Next, we organize these data into the BIDS structure. (3) Using DataLad, we version them, and (4) finally upload them to an open repository like DataVerse or potentially OpenNeuro.]
) <glacier>
`LSLAutoBIDS` is an open-source Python package developed and actively used by the Computational Cognitive Science Lab at the University of Stuttgart. It offers a modular and reproducible workflow tailored for studies using LSL based data acquisition, specifically targeting the integration of EEG and eye-tracking modalities. 

In this setup, participant-level EEG data streams, but also other LSL streams (e.g., motion tracking, mobile eye-tracking), are recorded using the LSL protocol @kothe_chkothepylsl_2025, which allows for sub-millisecond time-synchronization of heterogeneously sampled streams #revBene[and results in an XDF container file, most commonly via the `LSLRecorder` @noauthor_labstreaminglayerapp-labrecorder_2025 package]. Project metadata like authors, license, experimental description, but also dataverse details are specified in one central configuration-toml file, which is then used to retrieve these project-specific metadata during the conversion process. The recorded raw data streams are then converted into the Brain Imaging Data Structure (BIDS) @gorgolewski_brain_2016 standard using the `mnelab` @brunner_mnelab_2022, `pylsl`@kothe_chkothepylsl_2025, `mne`@gramfort_meg_2013, and `mne_bids` @appelhoff_mne-bids_2019 packages. #revManpa[The converted EEG data are then validated with the `BIDSValidator`, while non-BIDS files like project metadata, configuration files, and additional modalities such as eye-tracking data are listed in a `.bidsignore` file to exclude them from validation. Thus, we are compliant with the `BIDSValidator` for our output]. Once #revManpa[validated], the BIDS-compliant dataset is automatically deposited into a Dataverse repository, along with the experiment stimulus files and the raw source data.

In addition to LSL-based EEG data acquisition, `LSLAutoBIDS` supports the incorporation of non-LSL data. For example, in our use case, eye-tracking data are collected using the EyeLink 1000 Plus eye tracker simultaneously with EEG data collection, which produces proprietary Eyelink data format (EDF) files that cannot easily be streamed via LSL. Other examples are an electronic lab notebook record, log files of the experiment, and a compressed archive of the experimental code used in that individual session. `LSLAutoBIDS` accommodates these files as a secondary data modality currently implemented via user-defined folders, filename specifications, and regular expression matching, and is able to organize them within the appropriate BIDS subdirectories to publish them alongside EEG data.

Version control is integrated into the pipeline using DataLad @halchenko_datalad_2021, enabling precise tracking of all data and metadata changes across the research lifecycle, including modification or re-transformation of the individual files. Datalad is very powerful, but we use only the basic functionalities to simplify adoption for new users. We are not using the `datalad run` or `datalad rerun` capabilities, but are only concerned with the versioning of large files (`datalad save` and `datalad push`). The two minimal commands a user needs to know are `datalad clone` to checkout a repository and `datalad get` to actually download large files. This split between providing only symbolic links to all binary files first and only then explicitly downloading, e.g., a subset of the dataset, allows for easy exploration of terabyte-sized datasets.

After each recording session, the dataset is then uploaded to an initially private Dataverse repository, where it is persistently archived with the specified metadata under a DOI. After data collection is finished, the dataset can be publicly released and shared, potentially under a data sharing agreement.

The architecture of `LSLAutoBIDS` is deliberately designed to be extensible. While we developed this tool with our setup in mind (Eyelink1000, ANT Neuro EEG, VR-setups), we will continuously add new devices and allow for further customizability. Already now, additional files, such as behavioral data, audio recordings, or physiological signals, can be integrated by extending configuration templates and adding corresponding processing steps. This generalizability makes `LSLAutoBIDS` not just a tool for EEG and eye-tracking studies, but a proof of concept for broader multimodal data workflows in cognitive neuroscience.

#revBene[How do workflows like LSLAutoBIDS address the examples raised in the introduction? 1) If data is immediately versioned and archived, then overwritten data can always be recovered. 2) As experimental files are included in the archive for each subject, it is easy to find any changes in the experimental code during data recording. 3) Even if a student leaves without further documenting the dataset, it is already in a cleaned up state, including metadata, greatly simplifying further use of the data. 4) Training of new users is greatly simplified, manual copying data via e.g. USB sticks and other idiosyncratic workflows are no longer necessary.]


= Conclusion

Practicing open science by design and frontloading the conversion to a citable data publication efficiently addresses many hurdles researchers face in data collection and publishing. Not only is any recorded dataset immediately converted to BIDS, it also is archived, findable, shareable, backed up, and versioned. 

Whether the final dataset is publicly available or only used internally (e.g., due to privacy issues in non-defaced MRIs), we think such a workflow will be helpful to many laboratories.

= Code and Data Availability

The LSLAutoBIDS package is continuously developed and freely available: #link("https://github.com/s-ccs/LSLAutoBIDS") or via Zenodo #link("https://zenodo.org/records/15525822")[10.5281/zenodo.15525821].

= Conflict of Interest
The authors declare no conflicts of interest that may bias or could be perceived to bias this work.

= Funding

Funded by Deutsche Forschungsgemeinschaft (DFG, German Research Foundations) in the Emmy Noether Programme - Project-ID 538578433 - and Germany's Excellence Strategy EXC 2075 - 390740016.

#set par(justify: true, first-line-indent: 0pt);

// send behinger an email with your zotero to get access to the group
#bibliography(title: "Bibliography", style:"american-medical-association", "zotero.bib")
