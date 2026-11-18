# Prepare a Study Abroad Evidence Packet for a Supplement Notice

When an administrator asks for more evidence about an overseas study period, this skill helps an applicant see which records answer each question and which details still need confirmation.

## What it does

It prepares a response index keyed to the notice, a timeline with references to individual pages or messages, and a list of outstanding actions. It can draft an explanation for the applicant or a request for the issuing institution. On a second device it compares file contents and provenance before revisiting affected findings.

## Who it's for

Use this with an actual request for additional study records and a set of files or emails you authorize the agent to inspect. Keep personal records in your private workspace. The host needs access to the sources you select. If a mailbox or device is unavailable, the inventory records that gap.

## Install

```sh
npx skills add m1nga/study-evidence-packet
```

Try this in a compatible agent:

> Use $study-evidence-packet with this notice and the records in the folder I selected. Prepare the documents I can review today and list the items my institution must confirm.

## Example

A fictional notice asks for original grades. A receiving school lists six accepted credits, while the source transcript is missing. The response index cites the transfer entry for the credits and leaves the original-grade request open. The applicant gets a draft transcript request. If the original transcript arrives later, the skill updates that item and keeps the earlier transfer record with its own source reference.

## Design notes

A single document can answer one question and leave another open. Recording the exact passage, what it establishes and who can resolve a gap makes it easier for an applicant or a second reviewer to check the packet. Signed originals stay separate from working copies.

## Validation

The maintainer walked through synthetic cases covering a missing transcript, conflicting dates, general teaching policies, and a second device with duplicate and revised records. These checks exercise the instructions. Administrative decisions remain with the receiving authority.

## Author

Built by [Ming](https://github.com/m1nga).
