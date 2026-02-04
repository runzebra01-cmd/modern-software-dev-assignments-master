async function fetchJSON(url, options) {
  console.log(`Fetching: ${url}`);
  try {
    const res = await fetch(url, options);
    console.log(`Response status: ${res.status}`);
    if (!res.ok) {
      const errorText = await res.text();
      console.error(`Error response: ${errorText}`);
      throw new Error(errorText);
    }
    const data = await res.json();
    console.log(`Data received:`, data);
    return data;
  } catch (error) {
    console.error(`Fetch error:`, error);
    throw error;
  }
}

async function loadNotes(params = {}) {
  console.log('Loading notes...');
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const query = new URLSearchParams(params);
  
  try {
    const notes = await fetchJSON('/notes/?' + query.toString());
    console.log(`Loaded ${notes.length} notes`);
    
    for (const n of notes) {
      const li = document.createElement('li');
      li.className = 'note-item';
      
      const content = document.createElement('div');
      content.className = 'note-content';
      content.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
      
      const actions = document.createElement('div');
      actions.className = 'note-actions';
      
      // Delete button
      const deleteBtn = document.createElement('button');
      deleteBtn.textContent = 'Delete';
      deleteBtn.className = 'btn-danger';
      deleteBtn.onclick = async () => {
        if (confirm('Delete this note?')) {
          try {
            await fetchJSON(`/notes/${n.id}`, { method: 'DELETE' });
            loadNotes(params);
          } catch (error) {
            alert('Failed to delete note: ' + error.message);
          }
        }
      };
      
      actions.appendChild(deleteBtn);
      li.appendChild(content);
      li.appendChild(actions);
      list.appendChild(li);
    }
  } catch (error) {
    console.error('Failed to load notes:', error);
    list.innerHTML = '<li>Error loading notes: ' + error.message + '</li>';
  }
}

async function loadActions(params = {}) {
  console.log('Loading actions...');
  const list = document.getElementById('actions');
  list.innerHTML = '';
  
  const query = new URLSearchParams(params);
  
  try {
    const items = await fetchJSON('/action-items/?' + query.toString());
    console.log(`Loaded ${items.length} action items`);
    
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
          try {
            await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
            loadActions(params);
          } catch (error) {
            alert('Failed to complete action: ' + error.message);
          }
        };
        actions.appendChild(completeBtn);
      }
      
      // Delete button
      const deleteBtn = document.createElement('button');
      deleteBtn.textContent = 'Delete';
      deleteBtn.className = 'btn-danger';
      deleteBtn.onclick = async () => {
        if (confirm('Delete this action item?')) {
          try {
            await fetchJSON(`/action-items/${a.id}`, { method: 'DELETE' });
            loadActions(params);
          } catch (error) {
            alert('Failed to delete action: ' + error.message);
          }
        }
      };
      actions.appendChild(deleteBtn);
      
      li.appendChild(content);
      li.appendChild(actions);
      list.appendChild(li);
    }
  } catch (error) {
    console.error('Failed to load actions:', error);
    list.innerHTML = '<li>Error loading actions: ' + error.message + '</li>';
  }
}

window.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded, initializing...');
  
  // Note form
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('Note form submitted');
    
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
      console.error('Failed to create note:', error);
      alert('Failed to create note: ' + error.message);
    }
  });

  // Action form
  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('Action form submitted');
    
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
      console.error('Failed to create action:', error);
      alert('Failed to create action: ' + error.message);
    }
  });

  // Search functionality
  document.getElementById('note-search-btn').addEventListener('click', async () => {
    const q = document.getElementById('note-search').value;
    loadNotes({ q });
  });
  
  document.getElementById('clear-note-search')?.addEventListener('click', () => {
    document.getElementById('note-search').value = '';
    loadNotes();
  });

  // Action filter
  document.getElementById('filter-completed').addEventListener('change', (e) => {
    const checked = e.target.checked;
    loadActions({ completed: checked });
  });
  
  // Load initial data
  console.log('Loading initial data...');
  loadNotes();
  loadActions();
});

console.log('app.js loaded');