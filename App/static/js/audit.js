let currentAuditMethod = 'manual';
let currentBuilding = null;
let currentFloor = null;
let currentRoom = null;
let expectedAssets = [];
let scannedAssets = [];
let isRoomAuditActive = false;

let isScanning = false;
let scanBuffer = '';
let scanTimeout = null;
const SCAN_TIMEOUT_MS = 20;

function loadFloors() {
    const buildingSelect = document.getElementById('buildingSelect');
    currentBuilding = buildingSelect.value;
    
    currentFloor = null;
    currentRoom = null;
    
    if (currentBuilding && currentBuilding !== 'Select Building') {
        document.getElementById('floorSelectContainer').style.display = 'block';
        const floorSelect = document.getElementById('floorSelect');
        
        floorSelect.innerHTML = '<option selected>Select Floor</option>';
        
        fetch(`/api/floors/${currentBuilding}`)
            .then(response => response.json())
            .then(floors => {
                floors.forEach(floor => {
                    const option = document.createElement('option');
                    option.value = floor.floor_id;
                    option.textContent = floor.floor_name;
                    floorSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching floors:', error));
        
        hideElements(['roomSelectContainer', 'auditMethodButtons', 'searchContainer', 
                      'assetList', 'scannedAssetsList']);
    } else {
        hideElements(['floorSelectContainer', 'roomSelectContainer', 'auditMethodButtons',
                      'searchContainer', 'assetList', 'scannedAssetsList']);
    }
}

function loadRooms() {
    const floorSelect = document.getElementById('floorSelect');
    currentFloor = floorSelect.value;
    
    currentRoom = null;
    
    if (currentFloor && currentFloor !== 'Select Floor') {
        document.getElementById('roomSelectContainer').style.display = 'block';
        const roomSelect = document.getElementById('roomSelect');
        
        roomSelect.innerHTML = '<option selected>Select Room</option>';
        
        fetch(`/api/rooms/${currentFloor}`)
            .then(response => response.json())
            .then(rooms => {
                rooms.forEach(room => {
                    const option = document.createElement('option');
                    option.value = room.room_id;
                    option.textContent = room.room_name;
                    roomSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching rooms:', error));
        
        hideElements(['auditMethodButtons', 'searchContainer', 'assetList', 'scannedAssetsList']);
    } else {
        hideElements(['roomSelectContainer', 'auditMethodButtons', 'searchContainer', 
                      'assetList', 'scannedAssetsList']);
    }
}

function loadRoomAssets() {
    const roomSelect = document.getElementById('roomSelect');
    currentRoom = roomSelect.value;
    
    if (currentRoom && currentRoom != 'Select Room') {
        showElements(['auditMethodButtons', 'searchContainer']);
        
        fetch(`/api/assets/${currentRoom}`)
            .then(response => response.json())
            .then(assets => {
                expectedAssets = assets;
                
                expectedAssets.forEach(asset => {
                    asset.found = false;
                    
                    if (!asset.id && asset['id: ']) {
                        asset.id = asset['id: '];
                    }
                });
                
                displayExpectedAssets();
                showElements(['assetList', 'scannedAssetsList']);
            })
            .catch(error => console.error('Error fetching assets:', error));
    } else {
        hideElements(['auditMethodButtons', 'searchContainer', 'assetList', 'scannedAssetsList']);
    }
}

function displayExpectedAssets() {
    const tableBody = document.getElementById('expectedAssetsTableBody');
    tableBody.innerHTML = '';
    
    expectedAssets.forEach(asset => {
        const row = document.createElement('tr');
        
        appendCell(row, asset.description);
        
        const idCell = document.createElement('td');
        const assetId = asset.id || asset.asset_id || asset.assetId || 
                        (asset['id: '] ? asset['id: '] : null) || '1';
        idCell.textContent = assetId;
        row.appendChild(idCell);
        
        appendCell(row, `${asset.brand} ${asset.model}`);
        
        appendCell(row, asset.assignee_id);
        
        const statusCell = document.createElement('td');
        const statusIndicator = document.createElement('span');
        
        if (asset.status === 'present' || asset.status === 'Active') {
            statusIndicator.className = 'status-dot status-good';
            statusCell.appendChild(statusIndicator);
            statusCell.appendChild(document.createTextNode(' Active'));
        } else {
            statusIndicator.className = 'status-dot status-poor';
            statusCell.appendChild(statusIndicator);
            statusCell.appendChild(document.createTextNode(' ' + asset.status));
        }
        row.appendChild(statusCell);
        
        const lastUpdatedCell = document.createElement('td');
        const date = new Date(asset.last_update);
        lastUpdatedCell.textContent = date.toLocaleDateString();
        row.appendChild(lastUpdatedCell);
        
        const foundCell = document.createElement('td');
        foundCell.id = `found-status-${assetId}`;
        foundCell.className = asset.found ? 'found-yes' : 'found-no';
        foundCell.textContent = asset.found ? 'YES' : 'NO';
        row.appendChild(foundCell);
        
        tableBody.appendChild(row);
    });
    
    document.getElementById('scannedAssetsTableBody').innerHTML = '';
}

function appendCell(row, text) {
    const cell = document.createElement('td');
    cell.textContent = text;
    row.appendChild(cell);
    return cell;
}

function setAuditMethod(method) {
    stopAllScanningMethods();
    
    currentAuditMethod = method;
    
    document.querySelectorAll('.audit-method-btn').forEach(btn => {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-light');
    });

    const activeBtn = document.querySelector(`.audit-method-btn[onclick="setAuditMethod('${method}')"]`);
    if (activeBtn) {
        activeBtn.classList.remove('btn-light');
        activeBtn.classList.add('btn-primary');
    }

    updateScanningInterface();
    
    if (isRoomAuditActive) {
        startScanningMethod(method);
    }
}

function updateScanningInterface() {
    const manualSearchGroup = document.getElementById('manualSearchGroup');
    
    hideElements(['scanIndicator', 'rfidIndicator', 'qrIndicator']);
    
    if (currentAuditMethod === 'manual') {
        manualSearchGroup.style.display = 'flex';
        document.getElementById('searchInput').placeholder = "Enter asset ID or serial number...";
    } else {
        manualSearchGroup.style.display = 'none';
    }
    
    if (isRoomAuditActive) {
        const indicatorId = {
            'barcode': 'scanIndicator',
            'rfid': 'rfidIndicator',
            'qrcode': 'qrIndicator'
        }[currentAuditMethod];
        
        if (indicatorId) {
            const indicator = document.getElementById(indicatorId) || createScanningIndicator(currentAuditMethod);
            if (indicator) indicator.style.display = 'block';
        }
    }
}

function toggleRoomAudit() {
    if (!isRoomAuditActive) {
        startRoomAudit();
    } else {
        stopRoomAudit();
    }
}

function startRoomAudit() {
    isRoomAuditActive = true;
    
    const toggleButton = document.getElementById('toggleRoomAudit');
    toggleButton.textContent = 'Stop Room Audit';
    toggleButton.classList.remove('btn-success');
    toggleButton.classList.add('btn-danger');
    
    updateScanningInterface();
    startScanningMethod(currentAuditMethod);
    
    updateScanCounter();
}

function stopRoomAudit() {
    isRoomAuditActive = false;
    
    stopAllScanningMethods();
    
    const toggleButton = document.getElementById('toggleRoomAudit');
    toggleButton.textContent = 'Start Room Audit';
    toggleButton.classList.remove('btn-danger');
    toggleButton.classList.add('btn-success');
    
    updateScanningInterface();
}

function startScanningMethod(method) {
    if (!isRoomAuditActive) return;
    
    if (method === 'barcode') {
        startBarcodeScan();
    } else if (method === 'rfid') {
        startSimulatedScan('rfid');
    } else if (method === 'qrcode') {
        startSimulatedScan('qrcode');
    }
}

function stopAllScanningMethods() {
    if (isScanning) {
        stopBarcodeScan();
    }
    
    ['rfidSimulationInterval', 'qrSimulationInterval'].forEach(intervalId => {
        if (window[intervalId]) {
            clearInterval(window[intervalId]);
            window[intervalId] = null;
        }
    });
}

function createScanningIndicator(method) {
    const indicatorId = {
        'barcode': 'scanIndicator',
        'rfid': 'rfidIndicator',
        'qrcode': 'qrIndicator'
    }[method];
    
    if (!indicatorId || document.getElementById(indicatorId)) return null;
    
    const indicatorMessages = {
        'barcode': '<strong>Barcode scanning active</strong><br>Scan assets or select a different scanning method',
        'rfid': '<strong>RFID scanning active</strong><br>Please place RFID reader near assets to scan',
        'qrcode': '<strong>QR Code scanning active</strong><br>Point the camera at QR codes to scan'
    };
    
    const indicator = document.createElement('div');
    indicator.id = indicatorId;
    indicator.className = 'alert alert-info mb-3';
    indicator.innerHTML = indicatorMessages[method] || '';
    
    const searchContainer = document.getElementById('searchContainer');
    const toggleButton = document.getElementById('toggleRoomAudit');
    if (searchContainer && toggleButton) {
        searchContainer.insertBefore(indicator, toggleButton);
    }
    
    return indicator;
}

function startBarcodeScan() {
    if (!isRoomAuditActive || currentAuditMethod !== 'barcode') return;
    
    isScanning = true;
    scanBuffer = '';
    
    const scanIndicator = document.getElementById('scanIndicator') || createScanningIndicator('barcode');
    if (scanIndicator) scanIndicator.style.display = 'block';
    
    document.addEventListener('keypress', handleScannerInput);
}

function stopBarcodeScan() {
    if (!isScanning) return;
    
    isScanning = false;
    
    document.removeEventListener('keypress', handleScannerInput);
    
    const scanIndicator = document.getElementById('scanIndicator');
    if (scanIndicator) scanIndicator.style.display = 'none';
}

function handleScannerInput(e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        return;
    }
    
    if (scanTimeout) {
        clearTimeout(scanTimeout);
    }
    
    if (e.key === 'Enter') {
        processScanBuffer();
        return;
    }
    
    scanBuffer += e.key;
    
    scanTimeout = setTimeout(() => {
        if (scanBuffer.length > 0) {
            processScanBuffer();
        }
    }, SCAN_TIMEOUT_MS);
    
    e.preventDefault();
}

function processScanBuffer() {
    if (scanBuffer.length === 0) return;
    
    // First check if the asset is in the expected assets list for this room
    const assetInRoom = expectedAssets.find(a => 
        a.id === scanBuffer || 
        (a.barcode && a.barcode === scanBuffer)
    );
    
    if (assetInRoom) {
        markAssetAsFound(assetInRoom);
        showScanMessage(`Asset found: ${assetInRoom.description} (${assetInRoom.id})`, 'success');
    } else {
        // If not in expected list, check the database to see if it exists at all
        checkAssetInDatabase(scanBuffer);
    }
    
    scanBuffer = '';
}

async function checkAssetInDatabase(assetId) {
    try {
        const response = await fetch(`/api/asset/${assetId}`);
        
        if (response.ok) {
            // Asset exists in database but not in this room
            const asset = await response.json();
            
            // Add the asset to scanned assets with misplaced status
            addMisplacedAsset(asset);
            
            showScanMessage(
                `Asset found: ${asset.description || 'Unknown'} (${assetId}) - Not assigned to this room!`, 
                'warning'
            );
        } else {
            // Asset not found in database
            showScanMessage(`Unknown asset: ${assetId}`, 'warning');
            addUnexpectedAsset(assetId);
        }
    } catch (error) {
        console.error('Error checking asset in database:', error);
        showScanMessage(`Error checking asset: ${assetId}`, 'danger');
    }
}

function markAssetAsFound(asset) {
    asset.found = true;
    
    const assetId = asset.id || asset.asset_id || asset.assetId || 
                   (asset['id: '] ? asset['id: '] : null) || '1';
    
    const foundCell = document.getElementById(`found-status-${assetId}`);
    if (foundCell) {
        foundCell.className = 'found-yes';
        foundCell.textContent = 'YES';
    } else {
        const altFoundCell = document.getElementById(`found-status-${asset.id}`);
        if (altFoundCell) {
            altFoundCell.className = 'found-yes';
            altFoundCell.textContent = 'YES';
        }
    }
    
    if (!scannedAssets.find(a => {
        const aId = a.id || a.asset_id || a.assetId || (a['id: '] ? a['id: '] : null);
        const thisId = asset.id || asset.asset_id || asset.assetId || (asset['id: '] ? asset['id: '] : null);
        return aId === thisId;
    })) {
        scannedAssets.push(asset);
        updateScannedAssetsTable();
    }
    
    updateScanCounter();
}

function updateScanCounter() {
    const foundCount = expectedAssets.filter(asset => asset.found).length;
    const totalCount = expectedAssets.length;
    
    let scanCounter = document.getElementById('scanCounter');
    if (!scanCounter) {
        scanCounter = document.createElement('div');
        scanCounter.id = 'scanCounter';
        scanCounter.className = 'alert alert-primary mt-3';
        document.getElementById('assetList').insertBefore(scanCounter, document.getElementById('assetList').firstChild);
    }
    
    scanCounter.innerHTML = `<strong>Asset Scan Progress:</strong> ${foundCount} of ${totalCount} assets found (${Math.round(foundCount/totalCount*100)}%)`;
    
    if (foundCount === totalCount && totalCount > 0) {
        scanCounter.className = 'alert alert-success mt-3';
        scanCounter.innerHTML += '<br><strong>✓ All assets accounted for!</strong>';
    }
    
    scanCounter.style.display = 'block';
}

function showScanMessage(message, type) {
    let scanMessage = document.getElementById('scanMessage');
    
    if (!scanMessage) {
        scanMessage = document.createElement('div');
        scanMessage.id = 'scanMessage';
        document.getElementById('searchContainer').appendChild(scanMessage);
    } else {
        if (scanMessage.hideTimeout) {
            clearTimeout(scanMessage.hideTimeout);
        }
    }
    
    scanMessage.className = `alert alert-${type} mt-2`;
    scanMessage.textContent = message;
    scanMessage.style.display = 'block';
    
    scanMessage.hideTimeout = setTimeout(() => {
        scanMessage.style.display = 'none';
    }, 3000);
}

function addUnexpectedAsset(barcode) {
    const unexpectedAsset = {
        id: `UNK-${barcode.substring(0, 6)}`,
        barcode: barcode,
        description: 'Unexpected Asset',
        brand: 'Unknown',
        model: 'Unknown',
        status: 'unexpected',
        room_id: currentRoom,
        assignee_id: 'Unassigned',
        last_update: new Date().toISOString(),
        found: true
    };
    
    scannedAssets.push(unexpectedAsset);
    updateScannedAssetsTable();
}

function updateScannedAssetsTable() {
    const scannedTableBody = document.getElementById('scannedAssetsTableBody');
    scannedTableBody.innerHTML = '';
    
    const sortedAssets = [...scannedAssets].sort((a, b) => {
        // Sort by status first (unexpected and misplaced at the top)
        if (a.status === 'unexpected' && b.status !== 'unexpected') return -1;
        if (a.status !== 'unexpected' && b.status === 'unexpected') return 1;
        if (a.status === 'misplaced' && b.status !== 'misplaced') return -1;
        if (a.status !== 'misplaced' && b.status === 'misplaced') return 1;
        
        return new Date(b.last_update) - new Date(a.last_update);
    });
    
    sortedAssets.forEach(asset => {
        const row = document.createElement('tr');
        
        // Apply classes based on asset status
        if (asset.status === 'unexpected') {
            row.className = 'table-warning';
        } else if (asset.status === 'misplaced') {
            row.className = 'table-warning'; // Use same warning style for misplaced assets
        }
        
        appendCell(row, asset.description);
        
        const idCell = document.createElement('td');
        const assetId = asset.id || asset.asset_id || asset.assetId || 
                        (asset['id:'] ? asset['id:'] : null) || '1';
        idCell.textContent = assetId;
        row.appendChild(idCell);
        
        appendCell(row, `${asset.brand} ${asset.model}`);
        
        const locationCell = document.createElement('td');
        const roomSelect = document.getElementById('roomSelect');
        const currentRoomName = roomSelect ? 
            roomSelect.options[roomSelect.selectedIndex].textContent : 
            `Room ${currentRoom}`;
            
        if (asset.status === 'misplaced') {
            locationCell.innerHTML = `<span class="text-warning">Current: ${currentRoomName}</span><br>
                                     <small>Assigned: Room ${asset.room_id}</small>`;
        } else {
            locationCell.textContent = currentRoomName;
        }
        row.appendChild(locationCell);
        
        const statusCell = document.createElement('td');
        const statusIndicator = document.createElement('span');
        
        if (asset.status === 'unexpected') {
            statusIndicator.className = 'status-dot status-warning';
            statusCell.appendChild(statusIndicator);
            statusCell.appendChild(document.createTextNode(' Unexpected'));
        } else if (asset.status === 'misplaced') {
            statusIndicator.className = 'status-dot status-warning';
            statusCell.appendChild(statusIndicator);
            statusCell.appendChild(document.createTextNode(' Misplaced'));
        } else if (asset.status === 'present' || asset.status === 'Active') {
            statusIndicator.className = 'status-dot status-good';
            statusCell.appendChild(statusIndicator);
            statusCell.appendChild(document.createTextNode(' Active'));
        } else {
            statusIndicator.className = 'status-dot status-poor';
            statusCell.appendChild(statusIndicator);
            statusCell.appendChild(document.createTextNode(' ' + asset.status));
        }
        row.appendChild(statusCell);
        
        appendCell(row, asset.assignee_id);
        
        const lastUpdatedCell = document.createElement('td');
        const date = new Date(asset.last_update);
        lastUpdatedCell.textContent = date.toLocaleDateString();
        row.appendChild(lastUpdatedCell);
        
        scannedTableBody.appendChild(row);
    });
    
    if (scannedAssets.length > 0) {
        document.getElementById('scannedAssetsList').style.display = 'block';
    }
}

async function manualSearchAsset() {
    if (!isRoomAuditActive) {
        showScanMessage('Please start a room audit first', 'warning');
        return;
    }
    
    const searchInput = document.getElementById('searchInput');
    const assetId = searchInput.value.trim();
   
    if (!assetId) {
        showScanMessage('Please enter an asset ID', 'warning');
        return;
    }

    // First check if the asset is in the expected assets list for this room
    const assetInRoom = expectedAssets.find(a => {
        const aId = a.id || a.asset_id || a.assetId || (a['id:'] ? a['id:'] : null);
        return aId === assetId;
    });
    
    if (assetInRoom) {
        markAssetAsFound(assetInRoom);
        showScanMessage(`Asset found: ${assetInRoom.description} (${assetInRoom.id})`, 'success');
        searchInput.value = '';
        return;
    }

    try {
        const response = await fetch(`/api/asset/${assetId}`);
        
        if (response.ok) {
            // Asset exists in database but not in this room
            const asset = await response.json();
            
            // Add the asset to scanned assets with misplaced status
            addMisplacedAsset(asset);
            
            showScanMessage(
                `Asset found: ${asset.description || 'Unknown'} (${assetId}) - Not assigned to this room!`, 
                'warning'
            );
        } else {
            if (confirm(`Asset "${assetId}" not found in system. Add as unexpected?`)) {
                addUnexpectedAsset(assetId);
            }
        }
        
        searchInput.value = '';

    } catch (error) {
        console.error('Error searching for asset:', error);
        showScanMessage('An error occurred while searching for the asset', 'danger');
    }
}

function addMisplacedAsset(asset) {
    // Format the asset data to match our expected structure
    const assetId = asset.id || asset['id:'] || asset.asset_id || '';
    const formattedAsset = {
        id: assetId,
        description: asset.description || 'Unknown Asset',
        brand: asset.brand || 'Unknown',
        model: asset.model || 'Unknown',
        status: 'misplaced',
        room_id: asset.room_id || 'Unknown',
        assignee_id: asset.assignee_id || 'Unassigned',
        last_update: asset.last_update || new Date().toISOString(),
        found: true,
        actualRoom: currentRoom
    };
    
    scannedAssets.push(formattedAsset);
    updateScannedAssetsTable();
}

function hideElements(elementIds) {
    elementIds.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.style.display = 'none';
    });
}

function showElements(elementIds) {
    elementIds.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.style.display = id === 'auditMethodButtons' ? 'flex' : 'block';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggleRoomAudit');
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleRoomAudit);
    }
    
    const searchButton = document.getElementById('manualSearchButton');
    if (searchButton) {
        searchButton.addEventListener('click', manualSearchAsset);
    }
    
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                manualSearchAsset();
            }
        });
    }
    
    setAuditMethod('manual');
});