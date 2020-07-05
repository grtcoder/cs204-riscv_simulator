CS204 RISC-V Simulator Phase 1 and Phase 2

Group:

Adarsh Kumar -2018CSB1066

Akshay Gahlot -2018CSB1068

Ankit Bhadu -2018CSB1073

Divyanshu Mathpal-2018CSB1086

G Pradyumn -2018CSB1088

instruction to run 1.) pip freeze > requirements.txt 2.) python Master_runner.py Requirements:- ->code should not contain comments ->Labels cannot be of the form label:. ':' should be separated by space from label name ->Arguments of instructions should be comma separated ->Address registers as x0,x1,........,x10,....,x15,......,x29,.....,x31 and not by pseudo names.

Points to note: In gui the instruction visible in any stage say decode will be decoded when one presses "next". SP value is to be used as 125 and for loading address of data stored one can directly load its address rather than using la, by taking the value as 252. 252 is the starting address for data memory. Size of MEM is 100000 bits. 

output_all.rtf has all stats which were to be printed Reg_File.rtf displays values of all registers after every clock cycle printed in an orderly fashion. pip_regsout.rtf contains values inside pipeline registers for each clock cycle. Knob5.rtf displays pipeline registers information for a particular instruction of our interest choosen during execution by user. final_memory.rtf containes data memory at end of execution.

Testing code needs to be added in /pipelined/testing.asm.

About Gui: Pipelined: Execute is green whenever branch is taken. Whenever there is data forwarding its highlighted wherein data from cyan colored block is forwarded to red coloured block. Unpipelined: Input code in editor, press assemble and simulate, then go to simulator and press run. Double click to add a break. Other functions are self explanatory in the GUI.
Please dont forget to add two instructions in fall through code.
We have tested our simulator on three risc v codes:

Factorial /pipelined/fact.txt
Bubble sort /pipelined/sort.txt
Fibonacci /pipelined/fib.txt
Phase 3 work distribution:

Ankit Bhadu-> Pipelined Execution, Buffer Registers, Data forwarding, Output stat,reg,mem files and knobs, Bit addressible to Byte addressible conversion, Datapath formation.

Adarsh Kumar->Debugging of the whole code,counting and verification of output statistics(data_hazards,control_hazards e.t.c).

Akshay Gahlot-> Debugging of the whole code, Detection and handling of Control Hazards, Bit addressible to Byte addressible conversion.

Divyanshu Mathpal-> GUI, and control signal based implementation.

G Pradyumn -> Wrote the code for Data Stalling and BTB and integrated Branch Target Buffer to Data Forwarding and Data Stalling.

Phase 1 and 2 work distribution: Instruction Set-Adarsh,Ankit,Divyanshu,Pradyumn

ALU-Adarsh,Akshay

Memory and Register Read Write-Adarsh,Akshay

Machine code generation- ankit

Handling of Labels-Ankit,Akshay,Adarsh

Error handling- Ankit, Divyanshu

GUI-Divyanshu

IAG-Pradyumn

Decoder-Pradyumn, Divyanshu

GUI:- Phase1 :- Choose unpipelined execution, which would directly open the gui. The gui supports all the required features. Phase2 :- Choose pipelined execution, which would directly open the gui for pipelining The gui allows you to see the state at a particular clock cycle. Also it allows you to move back and forth from that point onwards.