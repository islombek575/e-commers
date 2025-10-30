from django import forms
from django.utils.safestring import mark_safe
import json

class KeyValueWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if not value:
            value = {}
        elif isinstance(value, str):
            try:
                value = json.loads(value)
            except Exception:
                value = {}

        rows = ""
        for k, v in value.items():
            rows += f"""
            <div class="kv-row" style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <input type="text" name="{name}_key" value="{k}" placeholder="Key" 
                       style="flex: 1; padding: 6px 8px; border-radius: 6px; border: 1px solid #ccc;">
                <input type="text" name="{name}_value" value="{v}" placeholder="Value"
                       style="flex: 2; padding: 6px 8px; border-radius: 6px; border: 1px solid #ccc;">
                <button type="button" class="kv-remove" onclick="this.parentNode.remove()" 
                        style="background: #ff4d4f; color: white; border: none; border-radius: 5px; padding: 4px 10px; cursor: pointer;">❌</button>
            </div>
            """

        html = f"""
        <div id="{name}_container">
            {rows}
        </div>

        <button type="button" onclick="addRow_{name}()" 
                style="margin-top: 6px; background: #1890ff; color: white; border: none;
                       border-radius: 6px; padding: 5px 10px; cursor: pointer;">➕ Qo‘shish</button>

        <input type="hidden" name="{name}" id="id_{name}_hidden">

        <script>
        function addRow_{name}() {{
            const c = document.getElementById("{name}_container");
            const div = document.createElement("div");
            div.classList.add("kv-row");
            div.style = "display:flex; align-items:center; gap:8px; margin-bottom:6px;";
            div.innerHTML = `
                <input type="text" name="{name}_key" placeholder="Key" 
                       style="flex:1; padding:6px 8px; border-radius:6px; border:1px solid #ccc;">
                <input type="text" name="{name}_value" placeholder="Value" 
                       style="flex:2; padding:6px 8px; border-radius:6px; border:1px solid #ccc;">
                <button type="button" class="kv-remove" onclick="this.parentNode.remove()" 
                        style="background:#ff4d4f; color:white; border:none; border-radius:5px; padding:4px 10px; cursor:pointer;">❌</button>
            `;
            c.appendChild(div);
        }}

        document.addEventListener("submit", function(e) {{
            const rows = document.querySelectorAll('#{name}_container .kv-row');
            let data = {{}};
            rows.forEach(r => {{
                const key = r.querySelector('input[name="{name}_key"]').value;
                const val = r.querySelector('input[name="{name}_value"]').value;
                if (key) data[key] = val;
            }});
            document.getElementById("id_{name}_hidden").value = JSON.stringify(data);
        }});
        </script>
        """

        return mark_safe(html)
