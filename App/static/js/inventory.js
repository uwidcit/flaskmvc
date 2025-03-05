// Function to load assets from the backend
async function loadAssets() {
    try {
        const response = await fetch('/api/assets');
        if (!response.ok) {
            throw new Error('Failed to fetch assets');
        }
        
        const assets = await response.json();
        displayAssets(assets);
    } catch (error) {
        console.error('Error loading assets:', error);
        document.getElementById('assetTableBody').innerHTML = 
            '<tr><td colspan="8" class="text-center">Error loading assets. Please try again later.</td></tr>';
    }
}

// Function to display assets in the table
function displayAssets(assets) {
    const tableBody = document.getElementById('assetTableBody');
    
    if (!assets || assets.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="8" class="text-center">No assets found</td></tr>';
        return;
    }
    
    tableBody.innerHTML = '';
    
    assets.forEach(asset => {
        const row = document.createElement('tr');
        
        // Determine asset description
        const description = asset.description || 'Unknown Asset';
        
        // Determine asset ID
        const assetId = asset.id || asset['id:'] || '';
        
        // Create row cells
        row.innerHTML = `
            <td>${description}</td>
            <td>${assetId}</td>
            <td>${asset.model || 'N/A'}</td>
            <td>${asset.room_id || 'N/A'}</td>
            <td>
                <span class="status-dot status-${asset.status === 'Active' ? 'good' : 'poor'}"></span>
                ${asset.status || 'Unknown'}
            </td>
            <td>${asset.assignee_id || 'Unassigned'}</td>
            <td>${formatDate(asset.last_update)}</td>
            <td>
                <a href="/asset/${assetId}" class="btn btn-sm btn-outline-primary">
                    <i class="bi bi-pencil"></i>
                </a>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Helper function to format date
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString();
    } catch (e) {
        return dateString;
    }
}

// Function to handle search
function handleSearch() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const rows = document.querySelectorAll('#assetTableBody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

// Sort table function
function sortTable(columnIndex) {
    const table = document.querySelector('.inventory-table table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Get all the icon elements in the table headers
    const icons = table.querySelectorAll('th i.bi');
    
    // Reset all icons to the default state
    icons.forEach(icon => {
        icon.classList.remove('bi-sort-up');
        icon.classList.add('bi-sort-down');
    });
    
    // Get the icon for the clicked column
    const icon = icons[columnIndex];
    
    // Determine sort direction
    const isAscending = icon.classList.contains('bi-sort-down');
    
    // Update icon
    if (isAscending) {
        icon.classList.remove('bi-sort-down');
        icon.classList.add('bi-sort-up');
    } else {
        icon.classList.remove('bi-sort-up');
        icon.classList.add('bi-sort-down');
    }
    
    // Sort the rows
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        return isAscending
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
    });
    
    // Reattach rows in the new order
    rows.forEach(row => tbody.appendChild(row));
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    // Load assets when page loads
    loadAssets();
    
    // Set up search functionality
    const searchButton = document.querySelector('.search-button');
    searchButton.addEventListener('click', handleSearch);
    
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('keyup', event => {
        if (event.key === 'Enter') {
            handleSearch();
        }
    });
});