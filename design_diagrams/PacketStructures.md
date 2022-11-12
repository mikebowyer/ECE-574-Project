# Control Packet Structure Diagram


## Packet Description
The packet structured designed is intended to be sent both back and forth between the security system (raspberry pi)
and the user interface (android app). 

## Packet Structure
The packet has a length of 1024 bytes. The left most byte is the control byte which indicates which 
part of the packet the security system or android app can ignore. 

If a bytes associated control byte is set to 0, then the setting in that byte was not set by the sender, 
indicating the reciever should ignore its value. 

| Byte Number | Byte Meaning           | Payload                                            | Enabling Control Byte Bit |
| ----------- | ---------------------- | -------------------------------------------------- | ------------------------- |
| 0x1023      | Control Byte           | 0x00 through 0x06                                  | N/A                       |
| ...         | ....                   | ...                                                | ...                       |
| 0x5         | Alarm triggering event | 0x00 Unknown, 0x01 Window/Door, 0x02 Motion Sensor | 6                         |
| 0x5         | Alarm is triggered     | 0x00 for off, 0xFF for on                          | 6                         |
| 0x4         | Alarm Audio Clip Enum  | Enumeration of Audio Clips (0-3)                   | 5                         |
| 0x3         | Light Color Blue       | 0x00-0xFF                                          | 4                         |
| 0x3         | Light Color Green      | 0x00-0xFF                                          | 4                         |
| 0x3         | Light Color Red        | 0x00-0xFF                                          | 4                         |
| 0x2         | Light Off Time minutes | 0x00 - 0x3C (0 minutes to 60 minutes)              | 3                         |
| 0x2         | Light Off Time hour    | 0x00 - 0x18 (0 hours to 24 hours)                  | 3                         |
| 0x2         | Light On Time minutes  | 0x00 - 0x3C (0 minutes to 60 minutes)              | 2                         |
| 0x2         | Light On Time hour     | 0x00 - 0x18 (0 hours to 24 hours)                  | 2                         |
| 0x1         | Light on/off setting   | 0x00 for off, 0xFF for on                          | 1                         |
| 0x0         | Alarm on/off setting   | 0x00 for off, 0xFF for on                          | 0                         |

## Examples of Packet Transmission
### Turn Lights On
| Byte Number | Byte Value |
| ----------- | ---------- |
| 0x1023      | 0x03       |
| 0x01        | 0xFF       |
### Turn Alarm On
| Byte Number | Byte Value |
| ----------- | ---------- |
| 0x1023      | 0x01`      |
| 0x00        | 0xFF       |
