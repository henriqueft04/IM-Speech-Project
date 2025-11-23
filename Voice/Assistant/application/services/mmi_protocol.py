"""
MMI (Multimodal Interaction) Protocol implementation.
Simplified to match C# working version.
"""

import html


def create_mmi_message(text: str, language: str = "pt-PT") -> str:
    """
    Create an MMI message for TTS following the exact C# format.

    Args:
        text: Text to speak
        language: Language code (default: pt-PT)

    Returns:
        Complete MMI XML message as string
    """
    # Escape the message text for XML
    escaped_text = html.escape(text)

    # Create the SSML content (escaped)
    ssml_escaped = (
        f'&lt;speak version="1.0" '
        f'xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        f'xsi:schemaLocation="http://www.w3.org/2001/10/synthesis http://www.w3.org/TR/speech-synthesis/synthesis.xsd" '
        f'xml:lang="{language}"&gt;'
        f'&lt;p&gt;{escaped_text}&lt;/p&gt;'
        f'&lt;/speak&gt;'
    )

    # Build the complete MMI message
    mmi_message = (
        '<mmi:mmi xmlns:mmi="http://www.w3.org/2008/04/mmi-arch" mmi:version="1.0">'
            '<mmi:startRequest mmi:context="ctx-1" mmi:requestId="text-1" mmi:source="APPSPEECH" mmi:target="IM">'
                '<mmi:data>'
                    '<emma:emma xmlns:emma="http://www.w3.org/2003/04/emma" emma:version="1.0">'
                        '<emma:interpretation emma:confidence="1" emma:id="text-" emma:medium="text" emma:mode="command" emma:start="0">'
                            f'<command>"{ssml_escaped}"</command>'
                        '</emma:interpretation>'
                    '</emma:emma>'
                '</mmi:data>'
            '</mmi:startRequest>'
        '</mmi:mmi>'
    )

    return mmi_message
