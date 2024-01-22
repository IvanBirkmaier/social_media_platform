## Verwendete Technologien für das Styling (Frontend):
- Tailwind
- Shadcn

## Bitte beachten bei kafka Init-Fehler (kafka/init/init.sh) 

- `init.sh` in `init` von `CRLF` auf `LS` stellen. Dass hat was damit zu tun, dass der Zeilenumbruch im Container (Linux/Ubuntu-Systeme) nicht ausgeführt werden kann. 