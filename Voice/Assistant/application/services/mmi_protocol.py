"""
MMI (Multimodal Interaction) Protocol implementation.
Simplified to match C# working version.
"""

import html
import json


def create_mmi_message(text: str, language: str = "pt-PT") -> str:
    """
    Create an MMI message for TTS using ExtensionNotification.

    Args:
        text: Text to speak
        language: Language code (default: pt-PT)

    Returns:
        Complete MMI XML message as string
    """
    command_json = json.dumps({"text": text})

    command_escaped = html.escape(command_json)

    mmi_message = (
        '<mmi:mmi xmlns:mmi="http://www.w3.org/2008/04/mmi-arch" mmi:version="1.0">'
            '<mmi:ExtensionNotification mmi:name="output" mmi:source="APP" mmi:target="SPEECHOUT">'
                '<mmi:data>'
                    '<emma:emma xmlns:emma="http://www.w3.org/2003/04/emma" emma:version="1.0">'
                        '<emma:interpretation emma:confidence="1" emma:id="text-" emma:medium="text" emma:mode="command" emma:start="0">'
                            f'<command>{command_escaped}</command>'
                        '</emma:interpretation>'
                    '</emma:emma>'
                '</mmi:data>'
            '</mmi:ExtensionNotification>'
        '</mmi:mmi>'
    )

    return mmi_message
