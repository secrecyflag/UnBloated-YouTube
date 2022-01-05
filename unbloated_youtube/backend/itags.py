"""
`itag` in YouTube is representing the quality a video is streaming on.
Credits: AgentOak: "https://gist.github.com/AgentOak/34d47c65b1d28829bb17c24c04a0096f".
HFR = High Frame Rate
"""

H264 = [266, 264, 137, 136, 135, 134, 133, 160]
H264_HFR = [305, 304, 299, 298]
VP9 = [313, 271, 248, 247, 244, 243, 242, 278]
VP9_HFR = [272, 315, 308, 303, 302]
VP9_HDR_HFR = [337, 336, 335, 334, 333, 332, 331, 330]
AV1 = [397, 396, 395, 394]
AV1_HFR = [402, 571, 401, 400, 399, 398]
AV1_HDR_HFR = [701, 700, 699, 698, 697, 696, 695, 694]

