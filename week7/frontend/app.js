async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function loadNotes(params = {}) {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const query = new URLSearchParams(params);
  const notes = await fetchJSON('/notes/?' + query.toString());
  for (const n of notes) {
    const li = document.createElement('li');
    li.className = 'note-item';
    
    const content = document.createElement('div');
    content.className = 'note-content';
    content.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
    
    const actions = document.createElement('div');
    actions.className = 'note-actions';
    
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.className = 'btn-danger';
    deleteBtn.onclick = async () => {
      if (confirm('Delete this note?')) {
        await fetchJSON(`/notes/${n.id}`, { method: 'DELETE' });
        loadNotes(params);
        loadActions(); // 刷新action items列表
      }
    };
    
    actions.appendChild(deleteBtn);
    li.appendChild(content);
    li.appendChild(actions);
    list.appendChild(li);
  }
}

async function loadActions(params = {}) {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  
  const query = new URLSearchParams(params);
  const items = await fetchJSON('/action-items/?' + query.toString());
  
  // 获取所有笔记用于显示标题
  const notes = await fetchJSON('/notes/');
  const noteMap = {};
  notes.forEach(n => noteMap[n.id] = n.title);
  
  for (const a of items) {
    const li = document.createElement('li');
    li.className = 'action-item';
    
    const content = document.createElement('div');
    content.className = 'action-item-content';
    
    // 显示action item内容和所属笔记
    let displayText = a.description;
    if (a.note_id && noteMap[a.note_id]) {
      displayText = `[${noteMap[a.note_id]}] ${a.description}`;
    }
    
    // 添加优先级、负责人等信息
    let metaInfo = [];
    if (a.priority) metaInfo.push(`优先级:${a.priority}`);
    if (a.assignee) metaInfo.push(`@${a.assignee}`);
    if (a.due_date) metaInfo.push(`截止:${a.due_date}`);
    
    if (metaInfo.length > 0) {
      displayText += ` (${metaInfo.join(', ')})`;
    }
    
    displayText += ` [${a.completed ? 'Completed' : 'Pending'}]`;
    content.textContent = displayText;
    
    const actions = document.createElement('div');
    actions.className = 'action-buttons';
    
    if (!a.completed) {
      const completeBtn = document.createElement('button');
      completeBtn.textContent = 'Complete';
      completeBtn.className = 'btn-success';
      completeBtn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions(params);
      };
      actions.appendChild(completeBtn);
    } else {
      const reopenBtn = document.createElement('button');
      reopenBtn.textContent = 'Reopen';
      reopenBtn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ completed: false }),
        });
        loadActions(params);
      };
      actions.appendChild(reopenBtn);
    }
    
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.className = 'btn-danger';
    deleteBtn.onclick = async () => {
      if (confirm('Delete this action item?')) {
        await fetchJSON(`/action-items/${a.id}`, { method: 'DELETE' });
        loadActions(params);
      }
    };
    actions.appendChild(deleteBtn);
    
    li.appendChild(content);
    li.appendChild(actions);
    list.appendChild(li);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  // Note form
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    try {
      await fetchJSON('/notes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content }),
      });
      e.target.reset();
      loadNotes();
      loadActions(); // 刷新行动项列表，显示自动提取的项目
    } catch (error) {
      alert('Failed to create note: ' + error.message);
    }
  });

  // Note search
  document.getElementById('note-search-btn').addEventListener('click', async () => {
    const q = document.getElementById('note-search').value;
    loadNotes({ q });
  });
  
  const clearNoteSearch = document.getElementById('clear-note-search');
  if (clearNoteSearch) {
    clearNoteSearch.addEventListener('click', () => {
      document.getElementById('note-search').value = '';
      loadNotes();
    });
  }

  // Action form
  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    try {
      await fetchJSON('/action-items/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description }),
      });
      e.target.reset();
      loadActions();
    } catch (error) {
      alert('Failed to create action item: ' + error.message);
    }
  });

  // Action filter
  document.getElementById('filter-completed').addEventListener('change', (e) => {
    const checked = e.target.checked;
    loadActions({ completed: checked });
  });
  
  // Load initial data
  loadNotes();
  loadActions();
});


