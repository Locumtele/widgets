"""
Add auto-height functionality to existing generated form
"""

def add_auto_height_to_form(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # JavaScript code to add height communication
    auto_height_js = '''
        // Auto-height iframe communication
        function sendHeightToParent() {
            if (window.parent !== window) {
                const height = Math.max(
                    document.body.scrollHeight,
                    document.body.offsetHeight,
                    document.documentElement.clientHeight,
                    document.documentElement.scrollHeight,
                    document.documentElement.offsetHeight
                );

                window.parent.postMessage({
                    type: 'resize',
                    height: height + 50  // Add padding
                }, '*');
            }
        }

        // Send height on load and form changes
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(sendHeightToParent, 100);

            // Send height when sections change
            const observer = new MutationObserver(sendHeightToParent);
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeFilter: ['class', 'style']
            });

            // Send height on form interactions
            document.addEventListener('change', () => setTimeout(sendHeightToParent, 100));
            document.addEventListener('click', () => setTimeout(sendHeightToParent, 100));
        });

        // Send height periodically (fallback)
        setInterval(sendHeightToParent, 2000);
'''

    # Insert auto-height JS before the closing script tag
    insertion_point = html_content.rfind('document.addEventListener(\'DOMContentLoaded\'')
    if insertion_point != -1:
        # Find the start of the script section
        script_start = html_content.rfind('<script>', 0, insertion_point)
        if script_start != -1:
            # Insert after the opening script tag
            script_content_start = html_content.find('>', script_start) + 1
            html_content = (
                html_content[:script_content_start] +
                auto_height_js +
                html_content[script_content_start:]
            )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Auto-height functionality added to {output_file}")

if __name__ == "__main__":
    add_auto_height_to_form(
        "surveys/weightloss/GLP1-screener-live.html",
        "surveys/weightloss/GLP1-screener-auto-height.html"
    )