// Short prose columns do most of the wrapping. Enforce the requested
// ten-word ceiling only where short words still crowd a rendered line.
// Keep text, emphasis, links and accessible reading order intact.
(() => {
  const blocks = 'p,li,h1,h2,h3,h4,figcaption,summary';
  const ignored = 'svg,script,style,select,option,[aria-hidden="true"]';
  let frame, active = true;

  function wordsIn(block) {
    const words = [];
    const walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.parentElement.closest(ignored) || node.parentElement.closest(blocks) !== block) continue;
      for (const match of node.textContent.matchAll(/\S+/gu)) {
        const range = document.createRange();
        range.setStart(node, match.index);
        range.setEnd(node, match.index + match[0].length);
        const rect = range.getClientRects()[0];
        if (rect?.width && rect.height) words.push({node, offset: match.index, top: rect.top});
      }
    }
    return words;
  }

  function wrap(block) {
    if (!block.getClientRects().length) return;
    // Recalculate from natural wrapping after resizing or changing text.
    block.querySelectorAll('br[data-word-limit]').forEach(br => br.remove());
    block.normalize();
    let words = wordsIn(block);
    const maximumBreaks = words.length;
    for (let pass = 0; pass < maximumBreaks; pass++) {
      let top = null, count = 0, overflow;
      for (const word of words) {
        if (top === null || Math.abs(word.top - top) > 3) {
          top = word.top;
          count = 0;
        }
        if (++count > 10) { overflow = word; break; }
      }
      if (!overflow) break;
      const tail = overflow.node.splitText(overflow.offset);
      const br = document.createElement('br');
      br.dataset.wordLimit = '';
      tail.before(br);
      words = wordsIn(block);
    }
  }

  const observer = new MutationObserver(records => {
    if (records.some(record => {
      const el = record.target.nodeType === Node.ELEMENT_NODE ? record.target : record.target.parentElement;
      if (!el || el.closest(ignored)) return false;
      return el.closest(blocks + ',details,dialog') || [...record.addedNodes].some(node =>
        node.nodeType === Node.ELEMENT_NODE && (node.matches(blocks) || node.querySelector(blocks)));
    })) schedule();
  });
  function observe() {
    if (active && document.body) observer.observe(document.body, {subtree:true, childList:true, characterData:true, attributes:true, attributeFilter:['open']});
  }
  function apply() {
    if (!active || !document.body) return;
    observer.disconnect();
    document.querySelectorAll(blocks).forEach(wrap);
    observe();
    // The linked market charts align after their explanatory text wraps.
    if (typeof scheduleProse === 'function') scheduleProse();
  }
  function schedule() {
    cancelAnimationFrame(frame);
    if (active) frame = requestAnimationFrame(apply);
  }
  document.fonts.ready.then(schedule);
  addEventListener('resize', schedule);
  document.addEventListener('toggle', schedule, true);
  addEventListener('pagehide', () => { active = false; cancelAnimationFrame(frame); observer.disconnect(); });
  addEventListener('pageshow', () => { active = true; schedule(); });
  observe();
})();
