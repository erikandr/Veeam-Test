# Veeam-Test

## This simple script implements synchronization of a Source folder and all it's contents with Destination(or Synchronization) folder and logs all actions into a log file located in Logs folder. All folder paths must be specified by user at the start of this script, as well as desired period of synchronization (in seconds).

## User is not required to create Source, Destination nor Logs folders, since script does it all.

## NOTE: I shall akcnowladge that using "time.sleep()" method to create an interval is not the best practice, since it is not very accurate and blocks excecution of other program functionalities (if this script would be integrated in other program), but for the sake of simpicity of this script, it wouldn't make a difference if intervals between synchronizations 1s early or 1s late and synchronization is the only functionality this script implements.
