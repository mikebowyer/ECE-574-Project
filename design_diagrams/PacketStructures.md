# Packet Structure Diagrams

## Current state of lights
Sender: Raspberry Pi
Header Length: 1 Byte
Payload Length: 1 Byte

| Packet Meaning | Header | Payload  |
| -------------- | ------ | -------- |
| Lights are on  | 0x0    | 1XXXXXXX |
| Lights of off  | 0x0    | 0XXXXXXX |

## Current state of alarm
Sender: Raspberry Pi
Header Length: 1 Byte
Payload Length: 1 Byte

| Packet Meaning | Header | Payload  |
| -------------- | ------ | -------- |
| Alarm is on    | 0x0    | 1XXXXXXX |
| Alarm is off   | 0x0    | 0XXXXXXX |

## Current state of alarm
Sender: Raspberry Pi
Header Length: 1 Byte
Payload Length: 1 Byte

| Packet Meaning | Header | Payload  |
| -------------- | ------ | -------- |
| Alarm is on    | 0x0    | 1XXXXXXX |
| Alarm is off   | 0x0    | 0XXXXXXX |

## Current state of Lights On/Off Time
Sender: Raspberry Pi
Header Length: 1 Byte
Payload Length: 1 Byte

| Packet Meaning | Header | Payload  |
| -------------- | ------ | -------- |
| Alarm is on    | 0x1    | 1XXXXXXX |
| Alarm is off   | 0x1    | 0XXXXXXX |