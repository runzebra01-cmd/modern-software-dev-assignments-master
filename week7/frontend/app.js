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
  for (const a of items) {
    const li = document.createElement('li');
    li.className = 'action-item';
    
    const content = document.createElement('div');
    content.className = 'action-item-content';
    content.textContent = `${a.description} [${a.completed ? 'Completed' : 'Pending'}]`;
    
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


