# SMART WATER STATION v5.1 — Firebase setup

## 1. Admin login
HMI only asks for password:

- Password: `000000`
- Internal Firebase account: `admin@pumpwatersys.local`

Create this Email/Password user in Firebase Authentication with password `000000`.
Then copy its UID into Realtime Database:

`/users/<ADMIN_UID>/role = "admin"`

The user never needs to type the email in the HMI.

## 2. ESP32 account
Create another Email/Password Firebase user:

`device@pumpwatersys.local`

Set its password to the value of `DEVICE_PASSWORD` in `ESP32-v5.1.ino`, then put:

`/users/<DEVICE_UID>/role = "device"`

Do not use the old database legacy token after deploying the new Rules.

## 3. Deploy Rules
Import `firebase-rules-v5.1.json` into Realtime Database Rules.

## 4. Data ownership
- ESP32 writes: status, metrics, history, logs, alarms.
- Admin HMI writes: control and settings; HMI can ACK alarms.
- ESP32 alone decides AUTO, relay, interlock, E-STOP and alarm CLEAR.

## 5. Alarm lifecycle
`ACTIVE -> ACKED -> CLEARED`

ACK is an HMI/Admin action. CLEAR is an ESP32 action after the physical condition disappears.

## 6. Metrics
Running hours, cycle count and total liters are loaded from `/system/metrics` at ESP32 boot and periodically saved back, so normal ESP32 reboot does not reset them.

## 7. E-STOP
The software E-STOP is latched by ESP32. For a real installation, a physical emergency-stop circuit should independently remove relay/contactor power; Firebase/HMI must not be the only safety layer.
