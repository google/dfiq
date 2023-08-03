---
hide:
  - navigation
  - toc
---
# Questions

**Questions are the core of DFIQ.** All other DFIQ components are relative to Questions: Approaches
describe how to answer the Questions, and Scenarios and Facets organize the Questions logically. Below
is an index of all the Questions that are defined as part of DFIQ.

Some quick facts about Questions in DFIQ:

- Questions should be small enough in scope that they can be readily answered
- A single Question can be reused in multiple different Facets
- If a Question has any Approaches defined, it will render as a link to the detailed Question page

!!! Note
    Not all the Questions have Approaches defined; in fact, most don't at the moment.
    If you'd like to contribute an idea for a new Question, or a new Approach for answering an
    existing Question, please [open an issue on GitHub](https://github.com/google/dfiq/issues).

## Questions Index

| ID          | Question                             | Tags | Approaches |
| ----------- | ------------------------------------ | ---- | ---------- |
| <span class="dfiqIdTag">Q1054</span> | What Launch Daemons are configured? | <span class="dfiqTag">macOS</span> <span class="dfiqTag">T1543.004</span>  | 0 |
| <span class="dfiqIdTag">Q1017</span> | Were any files collected into a container? |  | 0 |
| <span class="dfiqIdTag">Q1057</span> | What network logon scripts are configured? | <span class="dfiqTag">T1037.003</span> <span class="dfiqTag">Windows</span>  | 0 |
| <span class="dfiqIdTag">Q1050</span> | Are there any GCS buckets within the cloud project shared externally? |  | 0 |
| <span class="dfiqIdTag">Q1080</span> | How many external recipients does the email have? |  | 0 |
| <span class="dfiqIdTag">Q1074</span> | Were any system event logs cleared? | <span class="dfiqTag">T1070.001</span> <span class="dfiqTag">T1070.002</span> <span class="dfiqTag">Linux</span> <span class="dfiqTag">Windows</span> <span class="dfiqTag">macOS</span>  | 0 |
| <span class="dfiqIdTag">Q1065</span> | What files are referenced in Registry "Run" keys? | <span class="dfiqTag">T1547.001</span> <span class="dfiqTag">Windows</span>  | 0 |
| <span class="dfiqIdTag">Q1058</span> | What domain accounts have been created? | <span class="dfiqTag">T1136.002</span> <span class="dfiqTag">Windows</span>  | 0 |
| <span class="dfiqIdTag">Q1055</span> | What Windows logon scripts are configured? | <span class="dfiqTag">Windows</span> <span class="dfiqTag">T1037.001</span>  | 0 |
| <span class="dfiqIdTag">Q1072</span> | Did Chrome's DNS Prefetching cause a DNS query? | <span class="dfiqTag">Web Browser</span> <span class="dfiqTag">DNS</span>  | 0 |
| <span class="dfiqIdTag">Q1012</span> | What files were copied from a USB device to a computer? |  | 0 |
| <span class="dfiqIdTag">Q1014</span> | What files did the actor open on their computer? | <span class="dfiqTag">File Knowledge</span>  | 0 |
| <span class="dfiqIdTag">Q1019</span> | What web browsers were running at a given time? | <span class="dfiqTag">Web Browser</span>  | 0 |
| <span class="dfiqIdTag">Q1083</span> | Were any files sent via Bluetooth? | <span class="dfiqTag">T1011.001</span>  | 0 |
| <span class="dfiqIdTag">Q1075</span> | Is the recipient account controlled by the sender? |  | 0 |
| <span class="dfiqIdTag">Q1002</span> | What USB devices were attached to a computer? |  | 0 |
| <span class="dfiqIdTag">Q1028</span> | Was there specialized "anti-forensic" (or "privacy") software on a computer? |  | 0 |
| <span class="dfiqIdTag">Q1067</span> | What system services are installed? | <span class="dfiqTag">macOS</span> <span class="dfiqTag">Linux</span> <span class="dfiqTag">Windows</span>  | 0 |
| <span class="dfiqIdTag">Q1063</span> | What periodic scripts are configured? | <span class="dfiqTag">macOS</span>  | 0 |
| <span class="dfiqIdTag">Q1078</span> | Were the files copies? |  | 0 |
| <span class="dfiqIdTag">Q1027</span> | Are there any sudden changes in the number of files on a device? |  | 0 |
| <span class="dfiqIdTag">Q1041</span> | Are there any unexpected successful API calls from an unknown external IP address (including Tor Exit nodes, C2 tagged addresses)? |  | 0 |
| <span class="dfiqIdTag">Q1021</span> | What Chrome extensions are installed? | <span class="dfiqTag">Web Browser</span>  | 0 |
| <span class="dfiqIdTag">Q1069</span> | Are there any indications of dylib hijacking? | <span class="dfiqTag">macOS</span> <span class="dfiqTag">T1574.004</span>  | 0 |
| <span class="dfiqIdTag">Q1001</span> |  <a href="/questions/Q1001">What files were downloaded using a web browser?</a>  | <span class="dfiqTag">NTFS</span> <span class="dfiqTag">Safari</span> <span class="dfiqTag">USN Journal</span> <span class="dfiqTag">Windows</span> <span class="dfiqTag">macOS</span> <span class="dfiqTag">Edge</span> <span class="dfiqTag">SQLite</span> <span class="dfiqTag">Chrome</span> <span class="dfiqTag">Web Browser</span>  | 3 |
| <span class="dfiqIdTag">Q1004</span> | What screenshots were taken on a computer? |  | 0 |
| <span class="dfiqIdTag">Q1039</span> | Are there any detections of exposed service account credentials? |  | 0 |
| <span class="dfiqIdTag">Q1024</span> | Was an Incognito/Private browser session used? | <span class="dfiqTag">Web Browser</span>  | 0 |
| <span class="dfiqIdTag">Q1071</span> | Are there any indications of dynamic linker hijacking? | <span class="dfiqTag">T1574.006</span> <span class="dfiqTag">macOS</span> <span class="dfiqTag">Linux</span>  | 0 |
| <span class="dfiqIdTag">Q1005</span> | What files have ever been on a computer? |  | 0 |
| <span class="dfiqIdTag">Q1052</span> | What browser extensions (non-Chrome) are installed? | <span class="dfiqTag">Web Browser</span>  | 0 |
| <span class="dfiqIdTag">Q1056</span> | What login hooks are configured? | <span class="dfiqTag">macOS</span> <span class="dfiqTag">T1037.002</span>  | 0 |
| <span class="dfiqIdTag">Q1049</span> | Is there an unusual increase of traffic between resource in the cloud project? |  | 0 |
| <span class="dfiqIdTag">Q1015</span> | What syncing activities did external "cloud storage" applications do on a computer? |  | 0 |
| <span class="dfiqIdTag">Q1010</span> | What was printed from a computer? |  | 0 |
| <span class="dfiqIdTag">Q1006</span> | What files are present on a computer? |  | 0 |
| <span class="dfiqIdTag">Q1035</span> | Were any copies made of sensitive files? |  | 0 |
| <span class="dfiqIdTag">Q1025</span> | What external accounts has the actor used in their web browser? |  | 0 |
| <span class="dfiqIdTag">Q1047</span> | Are there any suspicious modifications to the cloud project firewall rules/policies? |  | 0 |
| <span class="dfiqIdTag">Q1003</span> | What files were copied from a computer to a USB device? |  | 0 |
| <span class="dfiqIdTag">Q1045</span> | Are there any unknown accounts created? |  | 0 |
| <span class="dfiqIdTag">Q1053</span> | What Launch Agents are configured? | <span class="dfiqTag">macOS</span> <span class="dfiqTag">T1543.001</span>  | 0 |
| <span class="dfiqIdTag">Q1016</span> | What files were sent externally via email attachments? |  | 0 |
| <span class="dfiqIdTag">Q1009</span> | What interactions with external cloud storage sites did the actor have using their web browser? |  | 0 |
| <span class="dfiqIdTag">Q1044</span> | Are there any unexpected resources created under the cloud project? |  | 0 |
| <span class="dfiqIdTag">Q1018</span> | What process made the DNS query? | <span class="dfiqTag">DNS</span>  | 0 |
| <span class="dfiqIdTag">Q1064</span> | What systemd timers are configured? | <span class="dfiqTag">T1053.006</span> <span class="dfiqTag">Linux</span>  | 0 |
| <span class="dfiqIdTag">Q1037</span> |  <a href="/questions/Q1037">Have there been any executions of PsExeSrv?</a>  | <span class="dfiqTag">Prefetch</span> <span class="dfiqTag">Event Logs</span> <span class="dfiqTag">Windows</span>  | 3 |
| <span class="dfiqIdTag">Q1079</span> | Is there a history of communication with the recipients? |  | 0 |
| <span class="dfiqIdTag">Q1038</span> | Were any files sent via CLI utilities? |  | 0 |
| <span class="dfiqIdTag">Q1036</span> |  <a href="/questions/Q1036">Have there been any executions of PsExec?</a>  | <span class="dfiqTag">Prefetch</span> <span class="dfiqTag">Event Logs</span> <span class="dfiqTag">Windows</span>  | 2 |
| <span class="dfiqIdTag">Q1008</span> | What programs are installed on a computer? |  | 0 |
| <span class="dfiqIdTag">Q1084</span> | What data was uploaded to a website via a web browser? |  | 0 |
| <span class="dfiqIdTag">Q1030</span> | Were any security or monitoring agents tampered with or disabled? |  | 0 |
| <span class="dfiqIdTag">Q1032</span> | What actions were taken in an Incognito (or "private") browser session? |  | 0 |
| <span class="dfiqIdTag">Q1070</span> | Are there any indications of dylib proxying? | <span class="dfiqTag">macOS</span>  | 0 |
| <span class="dfiqIdTag">Q1077</span> | Were there bulk downloads from Google Drive? |  | 0 |
| <span class="dfiqIdTag">Q1013</span> | What files are present on a USB device? |  | 0 |
| <span class="dfiqIdTag">Q1046</span> | Are there any unknown role bindings created? |  | 0 |
| <span class="dfiqIdTag">Q1023</span> | Is a given Chrome extension associated with a given domain? | <span class="dfiqTag">Chrome</span> <span class="dfiqTag">T1176</span>  | 0 |
| <span class="dfiqIdTag">Q1062</span> | What cron jobs are configured? | <span class="dfiqTag">macOS</span> <span class="dfiqTag">Linux</span> <span class="dfiqTag">T1053.003</span>  | 0 |
| <span class="dfiqIdTag">Q1059</span> | What local accounts have been created? | <span class="dfiqTag">T1136.001</span> <span class="dfiqTag">macOS</span> <span class="dfiqTag">Linux</span> <span class="dfiqTag">Windows</span>  | 0 |
| <span class="dfiqIdTag">Q1048</span> | Are there any suspicious modifications to the cloud project logging configuration? |  | 0 |
| <span class="dfiqIdTag">Q1060</span> | What AT jobs are configured? | <span class="dfiqTag">T1053.002</span> <span class="dfiqTag">macOS</span> <span class="dfiqTag">Linux</span>  | 0 |
| <span class="dfiqIdTag">Q1042</span> | Are there any APIs recently enabled? |  | 0 |
| <span class="dfiqIdTag">Q1051</span> | Are there any signs of data within the cloud project being transferred externally? |  | 0 |
| <span class="dfiqIdTag">Q1068</span> | When were system services last modified? | <span class="dfiqTag">macOS</span> <span class="dfiqTag">Linux</span> <span class="dfiqTag">Windows</span>  | 0 |
| <span class="dfiqIdTag">Q1082</span> | Were any files sent via AirDrop? |  | 0 |
| <span class="dfiqIdTag">Q1029</span> | Were any encryption programs used on a computer? |  | 0 |
| <span class="dfiqIdTag">Q1061</span> | What Scheduled Tasks are configured? | <span class="dfiqTag">Windows</span> <span class="dfiqTag">T1053.005</span>  | 0 |
| <span class="dfiqIdTag">Q1081</span> | Does the user have a recently provisioned host? |  | 0 |
| <span class="dfiqIdTag">Q1066</span> | What items are in startup folders? | <span class="dfiqTag">T1547.001</span> <span class="dfiqTag">Windows</span>  | 0 |
| <span class="dfiqIdTag">Q1026</span> | What files were downloaded from messaging apps? |  | 0 |
| <span class="dfiqIdTag">Q1020</span> |  <a href="/questions/Q1020">What pages did web browsers visit?</a>  | <span class="dfiqTag">Safari</span> <span class="dfiqTag">Internet Explorer</span> <span class="dfiqTag">Edge</span> <span class="dfiqTag">Firefox</span> <span class="dfiqTag">SQLite</span> <span class="dfiqTag">Chrome</span> <span class="dfiqTag">Web Browser</span>  | 1 |
| <span class="dfiqIdTag">Q1043</span> | Are there any role bindings to cluster admin for anonymous users? |  | 0 |
| <span class="dfiqIdTag">Q1040</span> | Are there any interaction with the cloud project resources from an unknown external IP address (including Tor Exit nodes, C2 tagged addresses)? |  | 0 |
| <span class="dfiqIdTag">Q1033</span> | Was shell history cleared? |  | 0 |
| <span class="dfiqIdTag">Q1073</span> | Have there been any modifications to the "hosts" file? |  | 0 |
| <span class="dfiqIdTag">Q1007</span> | What files were synced or backed-up to external services? | <span class="dfiqTag">T1567.002</span>  | 0 |
| <span class="dfiqIdTag">Q1076</span> | Were the files screenshots? |  | 0 |
| <span class="dfiqIdTag">Q1022</span> | What actions did a Chrome extension perform? | <span class="dfiqTag">Chrome</span> <span class="dfiqTag">Web Browser</span> <span class="dfiqTag">Browser Extension</span>  | 0 |
| <span class="dfiqIdTag">Q1011</span> | What files were sent or received by a chat application? |  | 0 |
| <span class="dfiqIdTag">Q1034</span> | Was content copied from a file? |  | 0 |
| <span class="dfiqIdTag">Q1031</span> | How much network traffic was there to/from a machine? |  | 0 |
