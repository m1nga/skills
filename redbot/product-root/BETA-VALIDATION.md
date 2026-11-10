# RedBot 1.8 — invitation-only account test

Checked 2026-11-03. Builder-operated tests and read-only account trials, not independent user research or proof of full-account coverage.

- 27 JavaScript tests, 23 Python connector fixtures and 3 legacy sync regression tests passed. Connector fixtures cover progressive persistence, more than 2,000 cards, stopping without data loss, restart recovery, deduplication, source-end evidence, identity and isolated sessions. Fixtures are not two real people.
- Targeted upstream Go tests and Node pagination-wire/identity fixtures passed, including the observed note/collect/page and note_id shape, explicit end signals, malformed pagination and delayed identity hydration.
- A synthetic browser account streamed 20 then 60 cards; browsing/search stayed usable, stop retained arrivals, and focused search and unsaved note drafts survived refreshes. This is a controlled fixture, not a real collection coverage result.
- The real account library retained 295 unique cards and one retrieved post text. A recent v7 scan observed 80 cards before a successful source envelope lacked pagination fields; it does not establish complete enumeration. Earlier diagnostic traffic included a valid has_more:false page after 290 cards. That single page does not prove the required complete response chain.
- The final v8 patch recognizes the observed wire shape and stops malformed pagination as source_response_incomplete. Automated fixtures passed; this exact final patch was not followed by another real full scan. No complete real-account claim is made.
- A real first batch of 20 arrived in about six seconds. One anonymous QR request took 3.77 seconds. These are individual observations, not timing guarantees. The existing real session recovered with its own cookies without a new QR confirmation.
- An actual 390-pixel Chrome viewport reported document width 390 with no horizontal overflow. Physical-phone sign-in, same-phone QR recognition, two distinct real accounts and unaided human trials remain unverified.

Only a valid source pagination chain starting at the initial cursor, ending explicitly with has_more:false and covering observed IDs permits a complete signal. Silence, unchanged counts, deadlines, errors, stop and malformed responses remain partial. There is no fixed card-count or scroll-count cap; a 45-second lack of new cards and a 30-minute request deadline still stop unconfirmed scans. Retry restarts from the top and deduplicates; omitted old saves remain.

Scanning and deduplication make no LLM calls. Post captions do not prove video, image or comment understanding. The host must remain online; retention is seven days. Browser notes/plans require export for transfer. Prior native Mac package and GitHub migration/export bridges are unchanged.

Application source: 40823da0edf40347e4d1918f0b01bf024d4f5630. Public package excludes private runtime, account content, credentials and binaries.

## 1.9.4 — all-content reading (2026-11-04)

- Executed: 99 application JavaScript tests; 96 distributed JavaScript tests (three historical private-research fixtures excluded); 67 Python tests; 9 companion reader tests.
- Actual Chrome, synthetic source/account: whole-library reading, pause, reload and resume, selected-video result, one failure then targeted retry, final 3/3 ready; 390px view without horizontal overflow.
- Actual local synthetic 661-second / 106,012,140-byte MP4 completed chunked audio and 12 OCR samples, with no cloud inference. Blank/silent media is not recognition-quality evidence.
- The original connected app browser was inspected and showed the user-selected SEO video ready. This does not certify all real saved content as processed. Three existing libraries and their sign-in credentials were retained; normal rescan can update list/checkpoint files.
- Queue has no saved-item-count cutoff. Source access, storage, login and deadlines can still fail. Completed content is reused and failures stay visible.
