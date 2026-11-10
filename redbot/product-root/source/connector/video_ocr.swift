import Foundation
import Vision
import ImageIO
let url = URL(fileURLWithPath: CommandLine.arguments[1])
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["zh-Hans", "en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: url).perform([request])
let rows = (request.results ?? []).compactMap { $0.topCandidates(1).first }.map { ["text": $0.string, "confidence": $0.confidence] as [String: Any] }
let data = try JSONSerialization.data(withJSONObject: rows)
print(String(data:data,encoding:.utf8)!)
