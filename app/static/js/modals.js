// globals
const svgCanvas = new $.SvgCanvas(document.getElementById("svgcanvas"));
const editor = new MD.Editor();
const state = new State();

editor.modal = {
  about: new MD.Modal({
    html: `
      <h1>About this application</h1>
      <p>EcoDesign is designed to streamline your workflow and enhance your creativity, ensuring that every project is not only visually stunning but also economically feasible. Whether you're tweaking a simple vector or designing intricate layouts, EcoDesign provides the tools you need to succeed. Upgrade to EcoDesign Premium for advanced features that help you push the boundaries of design and achieve meticulous, cost-effective results.</p>
      `
  }),
  source: new MD.Modal({
    html: `
      <div id="svg_source_editor">
        <div id="svg_source_overlay" class="overlay"></div>
        <div id="svg_source_container">
          <form>
            <textarea id="svg_source_textarea" spellcheck="false"></textarea>
          </form>
          <div id="tool_source_back" class="toolbar_button">
            <button id="tool_source_cancel" class="cancel">Cancel</button>
            <button id="tool_source_save" class="ok">Apply Changes</button>
          </div>
        </div>
    </div>`,
    js: function(el){
      el.children[0].classList.add("modal-item-source");
      el.querySelector("#tool_source_save").addEventListener("click", function(){
        var saveChanges = function() {
          svgCanvas.clearSelection();
          $('#svg_source_textarea').blur();
          editor.zoom.multiply(1);
          editor.rulers.update();
          editor.paintBox.fill.prep();
          editor.paintBox.stroke.prep();
          editor.modal.source.close();
        }

        if (!svgCanvas.setSvgString($('#svg_source_textarea').val())) {
          $.confirm("There were parsing errors in your SVG source.\nRevert back to original SVG source?", function(ok) {
            if(!ok) return false;
            saveChanges();
          });
        } else {
          saveChanges();
        } 
      })
      el.querySelector("#tool_source_cancel").addEventListener("click", function(){
        editor.modal.source.close();
      });
    }
  }),
  configure: new MD.Modal({
    html: `
      <h1>Configuration</h1>
      <div id="configuration">
        <button class="warning">Erase all data</button>
        </div>
      </div>`,
    js: function(el){
      const input = el.querySelector("#configuration button.warning");
      input.addEventListener("click", function(){
        state.clean();
      })
    }
  }),
  donate: new MD.Modal({
    html: `
      <h1>Donate</h1>
      <p>
        EcoDesign relies on your generous donations for continued development.
        <a href="https://method.ac/donate/">Donate now</a> if you find this application useful.
      </p>`
  }),
  shortcuts: new MD.Modal({
    html: `
      <h1>Shortcuts</h1>
      <div id="shortcuts"></div>`,
    js: function(el){
      el.children[0].classList.add("modal-item-wide");
    }
  })
};