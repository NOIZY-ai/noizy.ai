"""
NOIZY Fish — Embeddable Consent Widget
========================================

Embeddable JavaScript widget for displaying creator consent status.

Features:
- Consent badge showing license availability
- Quick inquiry form
- Real-time status updates
- Customizable styling
- Multiple display modes

Usage:
    <script src="https://api.noizyfish.io/widget.js"></script>
    <div id="noizy-consent" data-creator="NZ-CR-20260322-ABC123"></div>

Or dynamically:
    NoizyFish.widget({
        creator: 'NZ-CR-20260322-ABC123',
        target: '#consent-widget',
        theme: 'dark',
        showInquiry: true
    });
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class WidgetConfig:
    """Widget configuration."""
    creator_id: str
    theme: str = "light"  # light, dark, minimal
    show_inquiry: bool = True
    show_badge: bool = True
    show_rules: bool = False
    api_base: str = "https://api.noizyfish.io"
    on_inquiry: Optional[str] = None  # Callback function name


def generate_widget_js(api_base: str = "http://localhost:8765") -> str:
    """Generate the embeddable widget JavaScript."""
    return f'''
// NOIZY Fish Consent Widget
// Embed creator consent status on any website
(function() {{
    'use strict';

    const NOIZY_API = '{api_base}';

    // Widget styles
    const STYLES = `
        .noizy-widget {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            border: 1px solid #e1e4e8;
            border-radius: 8px;
            padding: 16px;
            max-width: 320px;
            background: #ffffff;
        }}
        .noizy-widget.dark {{
            background: #1a1a2e;
            border-color: #2d2d44;
            color: #e1e4e8;
        }}
        .noizy-widget.minimal {{
            border: none;
            padding: 8px;
            background: transparent;
        }}
        .noizy-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }}
        .noizy-logo {{
            width: 24px;
            height: 24px;
        }}
        .noizy-title {{
            font-size: 14px;
            font-weight: 600;
            color: inherit;
        }}
        .noizy-creator {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .noizy-badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }}
        .noizy-badge.verified {{
            background: #d4edda;
            color: #155724;
        }}
        .noizy-badge.unverified {{
            background: #fff3cd;
            color: #856404;
        }}
        .noizy-rules {{
            margin: 12px 0;
            padding: 8px;
            background: #f6f8fa;
            border-radius: 6px;
            font-size: 13px;
        }}
        .dark .noizy-rules {{
            background: #2d2d44;
        }}
        .noizy-rule {{
            display: flex;
            justify-content: space-between;
            padding: 4px 0;
            border-bottom: 1px solid #e1e4e8;
        }}
        .dark .noizy-rule {{
            border-color: #3d3d54;
        }}
        .noizy-rule:last-child {{
            border-bottom: none;
        }}
        .noizy-rule-decision {{
            font-weight: 500;
        }}
        .noizy-rule-decision.allowed {{
            color: #28a745;
        }}
        .noizy-rule-decision.denied {{
            color: #dc3545;
        }}
        .noizy-rule-decision.negotiable {{
            color: #ffc107;
        }}
        .noizy-inquiry-btn {{
            width: 100%;
            padding: 10px;
            margin-top: 12px;
            background: #0366d6;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .noizy-inquiry-btn:hover {{
            background: #0256b9;
        }}
        .dark .noizy-inquiry-btn {{
            background: #58a6ff;
            color: #0d1117;
        }}
        .noizy-footer {{
            margin-top: 12px;
            font-size: 11px;
            color: #6a737d;
            text-align: center;
        }}
        .dark .noizy-footer {{
            color: #8b949e;
        }}
        .noizy-loading {{
            text-align: center;
            padding: 20px;
            color: #6a737d;
        }}
        .noizy-error {{
            color: #dc3545;
            padding: 12px;
            text-align: center;
        }}
    `;

    // Inject styles
    function injectStyles() {{
        if (!document.getElementById('noizy-styles')) {{
            const style = document.createElement('style');
            style.id = 'noizy-styles';
            style.textContent = STYLES;
            document.head.appendChild(style);
        }}
    }}

    // Fetch creator data
    async function fetchCreator(creatorId) {{
        const response = await fetch(`${{NOIZY_API}}/creators/${{creatorId}}`);
        if (!response.ok) throw new Error('Creator not found');
        return response.json();
    }}

    // Render widget
    function renderWidget(container, data, config) {{
        const theme = config.theme || 'light';
        const showInquiry = config.showInquiry !== false;
        const showRules = config.showRules === true;

        // Badge based on verification
        const isVerified = data.verification_status === 'fully_verified' ||
                          data.verification_status === 'pro_verified';
        const badgeClass = isVerified ? 'verified' : 'unverified';
        const badgeText = isVerified ? '✓ Verified' : 'Unverified';

        // Build HTML
        let html = `
            <div class="noizy-widget ${{theme}}">
                <div class="noizy-header">
                    <svg class="noizy-logo" viewBox="0 0 24 24" fill="currentColor">
                        <circle cx="12" cy="12" r="10" fill="#0366d6"/>
                        <path d="M12 6v12M6 12h12" stroke="white" stroke-width="2"/>
                    </svg>
                    <span class="noizy-title">NOIZY Fish</span>
                </div>
                <div class="noizy-creator">${{data.display_name}}</div>
                <span class="noizy-badge ${{badgeClass}}">${{badgeText}}</span>
        `;

        // Rules summary
        if (showRules && data.consent_rules && data.consent_rules.length > 0) {{
            html += '<div class="noizy-rules">';
            data.consent_rules.slice(0, 5).forEach(rule => {{
                const decisionClass = rule.decision.includes('allowed') ? 'allowed' :
                                     rule.decision === 'denied' ? 'denied' : 'negotiable';
                html += `
                    <div class="noizy-rule">
                        <span>${{formatCategory(rule.use_category)}}</span>
                        <span class="noizy-rule-decision ${{decisionClass}}">${{formatDecision(rule.decision)}}</span>
                    </div>
                `;
            }});
            html += '</div>';
        }}

        // Inquiry button
        if (showInquiry) {{
            html += `
                <button class="noizy-inquiry-btn" onclick="NoizyFish.openInquiry('${{data.creator_id}}')">
                    Request License
                </button>
            `;
        }}

        html += `
                <div class="noizy-footer">
                    Powered by <a href="https://noizyfish.io" target="_blank">NOIZY Fish</a>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }}

    // Format category for display
    function formatCategory(cat) {{
        return cat.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }}

    // Format decision for display
    function formatDecision(decision) {{
        const map = {{
            'allowed': '✓ Open',
            'allowed_terms': '✓ Terms',
            'denied': '✗ No',
            'requires_approval': '? Review',
            'negotiable': '$ Negotiate'
        }};
        return map[decision] || decision;
    }}

    // Open inquiry modal
    function openInquiry(creatorId) {{
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;
        modal.innerHTML = `
            <div style="background: white; padding: 24px; border-radius: 12px; max-width: 400px; width: 90%;">
                <h3 style="margin: 0 0 16px;">Request License</h3>
                <form id="noizy-inquiry-form">
                    <input type="hidden" name="creator_id" value="${{creatorId}}">
                    <div style="margin-bottom: 12px;">
                        <label style="display: block; margin-bottom: 4px; font-size: 14px;">Your Name *</label>
                        <input type="text" name="requestor_name" required
                            style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
                    </div>
                    <div style="margin-bottom: 12px;">
                        <label style="display: block; margin-bottom: 4px; font-size: 14px;">Email *</label>
                        <input type="email" name="requestor_email" required
                            style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
                    </div>
                    <div style="margin-bottom: 12px;">
                        <label style="display: block; margin-bottom: 4px; font-size: 14px;">Use Type *</label>
                        <select name="use_category" required
                            style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                            <option value="sync_film">Film/TV Sync</option>
                            <option value="sync_ad">Advertising</option>
                            <option value="streaming">Streaming</option>
                            <option value="sample">Sampling</option>
                            <option value="remix">Remix</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <label style="display: block; margin-bottom: 4px; font-size: 14px;">Offered Amount ($)</label>
                        <input type="number" name="offered_amount" min="0" step="100"
                            style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
                    </div>
                    <div style="margin-bottom: 16px;">
                        <label style="display: block; margin-bottom: 4px; font-size: 14px;">Description</label>
                        <textarea name="context" rows="3"
                            style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;"></textarea>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button type="button" onclick="this.closest('div[style*=fixed]').remove()"
                            style="flex: 1; padding: 10px; background: #f1f3f5; border: none; border-radius: 6px; cursor: pointer;">
                            Cancel
                        </button>
                        <button type="submit"
                            style="flex: 1; padding: 10px; background: #0366d6; color: white; border: none; border-radius: 6px; cursor: pointer;">
                            Submit
                        </button>
                    </div>
                </form>
            </div>
        `;
        document.body.appendChild(modal);

        // Handle form submit
        modal.querySelector('form').addEventListener('submit', async (e) => {{
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            if (data.offered_amount) data.offered_amount = parseFloat(data.offered_amount);

            try {{
                const response = await fetch(`${{NOIZY_API}}/inquiries`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(data)
                }});
                const result = await response.json();

                if (result.status === 'APPROVED') {{
                    alert('✓ Inquiry approved! The creator will be in touch.');
                }} else if (result.status === 'DENIED') {{
                    alert('✗ This use is not available. Reason: ' + result.reasons.join(', '));
                }} else {{
                    alert('⏳ Inquiry submitted for review. The creator will respond soon.');
                }}
                modal.remove();
            }} catch (err) {{
                alert('Error submitting inquiry. Please try again.');
            }}
        }});

        // Close on background click
        modal.addEventListener('click', (e) => {{
            if (e.target === modal) modal.remove();
        }});
    }}

    // Initialize widget
    async function initWidget(element) {{
        const creatorId = element.dataset.creator;
        const theme = element.dataset.theme || 'light';
        const showInquiry = element.dataset.inquiry !== 'false';
        const showRules = element.dataset.rules === 'true';

        if (!creatorId) {{
            element.innerHTML = '<div class="noizy-error">Missing creator ID</div>';
            return;
        }}

        element.innerHTML = '<div class="noizy-loading">Loading...</div>';

        try {{
            const data = await fetchCreator(creatorId);
            renderWidget(element, data, {{ theme, showInquiry, showRules }});
        }} catch (err) {{
            element.innerHTML = `<div class="noizy-error">${{err.message}}</div>`;
        }}
    }}

    // Public API
    window.NoizyFish = {{
        init: function() {{
            injectStyles();
            document.querySelectorAll('[data-noizy-widget]').forEach(initWidget);
            document.querySelectorAll('#noizy-consent').forEach(initWidget);
        }},
        widget: function(config) {{
            injectStyles();
            const container = typeof config.target === 'string'
                ? document.querySelector(config.target)
                : config.target;
            if (!container) return;
            container.dataset.creator = config.creator;
            container.dataset.theme = config.theme || 'light';
            container.dataset.inquiry = config.showInquiry !== false ? 'true' : 'false';
            container.dataset.rules = config.showRules ? 'true' : 'false';
            initWidget(container);
        }},
        openInquiry: openInquiry
    }};

    // Auto-init on DOM ready
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', NoizyFish.init);
    }} else {{
        NoizyFish.init();
    }}
}})();
'''


def generate_widget_html_example(creator_id: str, api_base: str = "http://localhost:8765") -> str:
    """Generate example HTML page with widget."""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NOIZY Fish Consent Widget Demo</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        h1 {{
            color: #1a1a2e;
        }}
        .demo-section {{
            margin: 40px 0;
            padding: 24px;
            background: #f6f8fa;
            border-radius: 12px;
        }}
        .demo-row {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
    </style>
</head>
<body>
    <h1>NOIZY Fish Consent Widget</h1>
    <p>Embeddable widget showing creator consent status.</p>

    <div class="demo-section">
        <h2>Light Theme</h2>
        <div data-noizy-widget data-creator="{creator_id}" data-theme="light" data-rules="true"></div>
    </div>

    <div class="demo-section" style="background: #1a1a2e;">
        <h2 style="color: white;">Dark Theme</h2>
        <div data-noizy-widget data-creator="{creator_id}" data-theme="dark" data-rules="true"></div>
    </div>

    <div class="demo-section">
        <h2>Minimal (Badge Only)</h2>
        <div class="demo-row">
            <div data-noizy-widget data-creator="{creator_id}" data-theme="minimal" data-inquiry="false"></div>
        </div>
    </div>

    <div class="demo-section">
        <h2>Dynamic Initialization</h2>
        <div id="dynamic-widget"></div>
        <script>
            // Dynamic widget initialization
            setTimeout(() => {{
                NoizyFish.widget({{
                    creator: '{creator_id}',
                    target: '#dynamic-widget',
                    theme: 'light',
                    showInquiry: true,
                    showRules: true
                }});
            }}, 100);
        </script>
    </div>

    <h2>Usage</h2>
    <pre style="background: #1a1a2e; color: #e1e4e8; padding: 16px; border-radius: 8px; overflow-x: auto;">
&lt;!-- Include widget script --&gt;
&lt;script src="{api_base}/widget.js"&gt;&lt;/script&gt;

&lt;!-- Add widget container --&gt;
&lt;div data-noizy-widget
     data-creator="{creator_id}"
     data-theme="light"
     data-rules="true"&gt;
&lt;/div&gt;

&lt;!-- Or initialize dynamically --&gt;
&lt;script&gt;
NoizyFish.widget({{
    creator: '{creator_id}',
    target: '#my-widget',
    theme: 'dark',
    showInquiry: true
}});
&lt;/script&gt;
    </pre>

    <!-- Widget script -->
    <script>
{generate_widget_js(api_base)}
    </script>
</body>
</html>
'''


def create_widget_routes(app, api_base: str = "http://localhost:8765"):
    """Add widget routes to a FastAPI app."""
    from fastapi.responses import Response, HTMLResponse

    @app.get("/widget.js")
    async def widget_script():
        """Get the embeddable widget JavaScript."""
        js = generate_widget_js(api_base)
        return Response(content=js, media_type="application/javascript")

    @app.get("/widget/demo")
    async def widget_demo(creator: str = None):
        """Widget demo page."""
        # Get a creator ID if not provided
        if not creator:
            from .registry import NoizyFishDB
            db = NoizyFishDB()
            creators = db.search_creators(limit=1)
            if creators:
                creator = creators[0]["creator_id"]
            else:
                creator = "demo-creator"

        html = generate_widget_html_example(creator, api_base)
        return HTMLResponse(content=html)

    return app


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate widget generation."""
    print("\n" + "=" * 70)
    print("NOIZY FISH CONSENT WIDGET — DEMO")
    print("=" * 70)

    print("\n" + "─" * 50)
    print("WIDGET JAVASCRIPT")
    print("─" * 50)

    js = generate_widget_js()
    print(f"  Generated {len(js):,} characters of JavaScript")
    print(f"  Preview (first 200 chars):")
    print(f"  {js[:200]}...")

    print("\n" + "─" * 50)
    print("EXAMPLE HTML")
    print("─" * 50)

    html = generate_widget_html_example("NZ-CR-20260322-ABC123")
    print(f"  Generated {len(html):,} characters of HTML")

    print("\n" + "─" * 50)
    print("USAGE")
    print("─" * 50)
    print('''
  1. Add script to page:
     <script src="http://localhost:8765/widget.js"></script>

  2. Add widget container:
     <div data-noizy-widget data-creator="NZ-CR-20260322-ABC123"></div>

  3. Or initialize dynamically:
     NoizyFish.widget({
         creator: 'NZ-CR-20260322-ABC123',
         target: '#widget',
         theme: 'dark'
     });

  Demo page available at:
     http://localhost:8765/widget/demo
    ''')

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo()
