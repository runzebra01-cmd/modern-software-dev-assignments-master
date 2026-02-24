async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  // Handle 204 No Content or empty responses
  if (res.status === 204 || res.headers.get('content-length') === '0') {
    return null;
  }
  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

// 全局标签列表缓存
let allTags = [];

async function loadAllTags() {
  allTags = await fetchJSON('/tags/');
  return allTags;
}

// 显示按标签筛选的笔记
async function displayFilteredNotes(notes, tagName) {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  
  // 添加筛选提示和清除按钮
  const header = document.createElement('div');
  header.className = 'filter-header';
  header.innerHTML = `<span>🔖 筛选: "${tagName}" (${notes.length}条)</span>`;
  const clearBtn = document.createElement('button');
  clearBtn.textContent = '显示全部';
  clearBtn.onclick = () => loadNotes();
  header.appendChild(clearBtn);
  list.appendChild(header);
  
  for (const n of notes) {
    const li = document.createElement('li');
    li.className = 'note-item';
    
    // 获取该笔记的标签
    let noteTags = n.tags || [];
    
    const content = document.createElement('div');
    content.className = 'note-content';
    content.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
    
    // 显示标签（可点击移除）
    if (noteTags.length > 0) {
      const tagsContainer = document.createElement('span');
      tagsContainer.className = 'note-tags';
      for (const t of noteTags) {
        const badge = document.createElement('span');
        badge.className = 'tag-badge';
        badge.style.background = t.color || '#ccc';
        badge.textContent = t.name;
        tagsContainer.appendChild(badge);
      }
      content.appendChild(tagsContainer);
    }
    
    li.appendChild(content);
    list.appendChild(li);
  }
}

async function loadNotes(params = {}) {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const query = new URLSearchParams(params);
  const notes = await fetchJSON('/notes/?' + query.toString());
  
  // 确保有标签数据
  if (allTags.length === 0) {
    await loadAllTags();
  }
  
  // 批量获取所有笔记的标签（避免N+1查询）
  const notesWithTags = await Promise.all(
    notes.map(async n => {
      try {
        const noteWithTags = await fetchJSON(`/notes/${n.id}/with-tags`);
        return { ...n, tags: noteWithTags.tags || [] };
      } catch (e) {
        return { ...n, tags: [] };
      }
    })
  );
  
  for (const n of notesWithTags) {
    const li = document.createElement('li');
    li.className = 'note-item';
    
    const noteTags = n.tags || [];
    
    const content = document.createElement('div');
    content.className = 'note-content';
    content.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
    
    // 显示标签（可点击移除）
    if (noteTags.length > 0) {
      const tagsContainer = document.createElement('span');
      tagsContainer.className = 'note-tags';
      for (const t of noteTags) {
        const badge = document.createElement('span');
        badge.className = 'tag-badge removable';
        badge.style.background = t.color || '#ccc';
        badge.innerHTML = `${t.name} <span class="remove-tag">×</span>`;
        badge.title = '点击移除标签';
        badge.onclick = async () => {
          if (confirm(`从笔记中移除标签 "${t.name}"?`)) {
            try {
              const res = await fetch(`/tags/${t.id}/notes/${n.id}`, { method: 'DELETE' });
              if (!res.ok) {
                throw new Error(await res.text() || res.statusText);
              }
              loadNotes(params);
            } catch (e) {
              console.error('Failed to remove tag:', e);
              alert('移除标签失败: ' + e.message);
            }
          }
        };
        tagsContainer.appendChild(badge);
      }
      content.appendChild(tagsContainer);
    }
    
    const actions = document.createElement('div');
    actions.className = 'note-actions';
    
    // 标签选择下拉框
    const tagSelect = document.createElement('select');
    tagSelect.className = 'tag-select';
    tagSelect.innerHTML = '<option value="">+ Tag</option>' + 
      allTags.map(t => `<option value="${t.id}">${t.name}</option>`).join('');
    tagSelect.onchange = async () => {
      const tagId = tagSelect.value;
      if (tagId) {
        try {
          await fetchJSON(`/tags/${tagId}/notes/${n.id}`, { method: 'POST' });
          loadNotes(params);
        } catch (e) {
          console.error('Failed to add tag:', e);
          alert('标签已存在或添加失败: ' + e.message);
        }
        tagSelect.value = '';
      }
    };
    
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.className = 'btn-danger';
    deleteBtn.onclick = async () => {
      if (confirm('Delete this note?')) {
        try {
          await fetchJSON(`/notes/${n.id}`, { method: 'DELETE' });
          loadNotes(params);
          loadActions();
        } catch (e) {
          console.error('Failed to delete note:', e);
          alert('删除笔记失败: ' + e.message);
        }
      }
    };
    
    actions.appendChild(tagSelect);
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

// Tag functions (Task 3)
async function loadTags() {
  const list = document.getElementById('tags');
  if (!list) return;
  list.innerHTML = '';
  
  const tags = await fetchJSON('/tags/');
  allTags = tags; // 更新全局标签缓存
  
  for (const tag of tags) {
    const li = document.createElement('li');
    li.className = 'tag-item';
    li.style.borderLeft = `4px solid ${tag.color || '#ccc'}`;
    
    const content = document.createElement('span');
    content.className = 'tag-name';
    content.textContent = tag.name;
    content.style.color = tag.color || '#333';
    
    const actions = document.createElement('div');
    actions.className = 'tag-actions';
    
    // 筛选按钮 - 按标签筛选笔记
    const filterBtn = document.createElement('button');
    filterBtn.textContent = '筛选';
    filterBtn.className = 'btn-primary';
    filterBtn.title = '显示带有此标签的笔记';
    filterBtn.onclick = async () => {
      // 获取该标签下的笔记
      const notesWithTag = await fetchJSON(`/tags/${tag.id}/notes`);
      displayFilteredNotes(notesWithTag, tag.name);
    };
    
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.className = 'btn-danger';
    deleteBtn.onclick = async () => {
      if (confirm(`Delete tag "${tag.name}"?`)) {
        try {
          await fetchJSON(`/tags/${tag.id}`, { method: 'DELETE' });
          loadTags();
          loadNotes(); // 刷新笔记列表以更新标签显示
        } catch (e) {
          console.error('Failed to delete tag:', e);
          alert('删除标签失败: ' + e.message);
        }
      }
    };
    
    actions.appendChild(filterBtn);
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
  
  // Tag form (Task 3)
  const tagForm = document.getElementById('tag-form');
  if (tagForm) {
    tagForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('tag-name').value;
      const color = document.getElementById('tag-color').value;
      try {
        await fetchJSON('/tags/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, color }),
        });
        e.target.reset();
        document.getElementById('tag-color').value = '#3498db'; // Reset color
        loadTags();
        loadNotes(); // 刷新笔记列表以显示新标签选项
      } catch (error) {
        alert('Failed to create tag: ' + error.message);
      }
    });
  }
  
  // Load initial data - 先加载标签，再加载笔记
  loadTags().then(() => {
    loadNotes();
    loadActions();
  });
});


