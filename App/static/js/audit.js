let currentAuditMethod = 'manual';
        let currentBuilding = null;
        let currentFloor = null;
        let currentRoom = null;
        let expectedAssets = [];
        let scannedAssets = [];
        
        function loadFloors() {
            const buildingSelect = document.getElementById('buildingSelect');
            currentBuilding = buildingSelect.value;
            
            // Reset floor and room selections
            currentFloor = null;
            currentRoom = null;
            
            if (currentBuilding && currentBuilding !== 'Select Building') {
                // Show floor select and populate options
                document.getElementById('floorSelectContainer').style.display = 'block';
                const floorSelect = document.getElementById('floorSelect');
                
                // Clear existing options
                floorSelect.innerHTML = '<option selected>Select Floor</option>';
                
                // Fetch floors from API
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
                
                // Hide room select and subsequent elements
                document.getElementById('roomSelectContainer').style.display = 'none';
                document.getElementById('auditMethodButtons').style.display = 'none';
                document.getElementById('searchContainer').style.display = 'none';
                document.getElementById('assetList').style.display = 'none';
                document.getElementById('scannedAssetsList').style.display = 'none';
            } else {
                // Hide all dependent elements
                document.getElementById('floorSelectContainer').style.display = 'none';
                document.getElementById('roomSelectContainer').style.display = 'none';
                document.getElementById('auditMethodButtons').style.display = 'none';
                document.getElementById('searchContainer').style.display = 'none';
                document.getElementById('assetList').style.display = 'none';
                document.getElementById('scannedAssetsList').style.display = 'none';
            }
        }
        
        function loadRooms() {
            const floorSelect = document.getElementById('floorSelect');
            currentFloor = floorSelect.value;
            
            // Reset room selection
            currentRoom = null;
            
            if (currentFloor && currentFloor !== 'Select Floor') {
                // Show room select and populate options
                document.getElementById('roomSelectContainer').style.display = 'block';
                const roomSelect = document.getElementById('roomSelect');
                
                // Clear existing options
                roomSelect.innerHTML = '<option selected>Select Room</option>';
                
                // Fetch rooms from API
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
                
                // Hide subsequent elements
                document.getElementById('auditMethodButtons').style.display = 'none';
                document.getElementById('searchContainer').style.display = 'none';
                document.getElementById('assetList').style.display = 'none';
                document.getElementById('scannedAssetsList').style.display = 'none';
            } else {
                // Hide dependent elements
                document.getElementById('roomSelectContainer').style.display = 'none';
                document.getElementById('auditMethodButtons').style.display = 'none';
                document.getElementById('searchContainer').style.display = 'none';
                document.getElementById('assetList').style.display = 'none';
                document.getElementById('scannedAssetsList').style.display = 'none';
            }
        }
        
        function loadRoomAssets() {
            const roomSelect = document.getElementById('roomSelect');
            currentRoom = roomSelect.value;
            
            if (currentRoom && currentRoom != 'Select Room') {
                // Show audit method buttons
                document.getElementById('auditMethodButtons').style.display = 'flex';
                document.getElementById('searchContainer').style.display = 'flex';
                
                // Fetch assets for this room
                fetch(`/api/assets/${currentRoom}`)
                    .then(response => response.json())
                    .then(assets => {
                        expectedAssets = assets;
                        
                        // Reset the found status for all assets
                        expectedAssets.forEach(asset => {
                            asset.found = false;
                        });
                        
                        // Display assets
                        displayExpectedAssets();
                        
                        // Show asset lists
                        document.getElementById('assetList').style.display = 'block';
                        document.getElementById('scannedAssetsList').style.display = 'block';
                    })
                    .catch(error => console.error('Error fetching assets:', error));
            } else {
                document.getElementById('auditMethodButtons').style.display = 'none';
                document.getElementById('searchContainer').style.display = 'none';
                document.getElementById('assetList').style.display = 'none';
                document.getElementById('scannedAssetsList').style.display = 'none';
            }
        }
        
        function displayExpectedAssets() {
            const tableBody = document.getElementById('expectedAssetsTableBody');
            tableBody.innerHTML = '';
            
            expectedAssets.forEach(asset => {
                const row = document.createElement('tr');
                
                // Description
                const descCell = document.createElement('td');
                descCell.textContent = asset.description;
                row.appendChild(descCell);
                
                // Asset ID
                const idCell = document.createElement('td');
                idCell.textContent = asset.id;
                row.appendChild(idCell);
                
                // Brand/Model
                const brandModelCell = document.createElement('td');
                brandModelCell.textContent = `${asset.brand} ${asset.model}`;
                row.appendChild(brandModelCell);
                
                // Assignee - would need to fetch assignee details separately
                const assigneeCell = document.createElement('td');
                assigneeCell.textContent = asset.assignee_id; // Need to display assignee name instead of ID
                row.appendChild(assigneeCell);
                
                // Status
                const statusCell = document.createElement('td');
                const statusIndicator = document.createElement('span');
                
                if (asset.status === 'present') {
                    statusIndicator.className = 'status-dot status-good';
                    statusCell.appendChild(statusIndicator);
                    statusCell.appendChild(document.createTextNode(' Present'));
                } else {
                    statusIndicator.className = 'status-dot status-poor';
                    statusCell.appendChild(statusIndicator);
                    statusCell.appendChild(document.createTextNode(' ' + asset.status));
                }
                row.appendChild(statusCell);
                
                // Last Updated
                const lastUpdatedCell = document.createElement('td');
                const date = new Date(asset.last_update);
                lastUpdatedCell.textContent = date.toLocaleDateString();
                row.appendChild(lastUpdatedCell);
                
                // Found Status
                const foundCell = document.createElement('td');
                foundCell.id = `found-status-${asset.id}`;
                foundCell.className = asset.found ? 'found-yes' : 'found-no';
                foundCell.textContent = asset.found ? 'YES' : 'NO';
                row.appendChild(foundCell);
                
                tableBody.appendChild(row);
            });
            
            // Clear the scanned assets table
            document.getElementById('scannedAssetsTableBody').innerHTML = '';
        }
        
        function setAuditMethod(method) {
            currentAuditMethod = method;
            
            document.querySelectorAll('.audit-method-btn').forEach(btn => {
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-light');
            });

            const activeBtn = document.querySelector(`.audit-method-btn[onclick="setAuditMethod('${method}')"]`);
            activeBtn.classList.remove('btn-light');
            activeBtn.classList.add('btn-primary');

            // Show search bar only for manual mode
            const searchInput = document.getElementById('searchInput');
            if (method === 'manual') {
                searchInput.style.display = 'block';
                searchInput.placeholder = "Search assets manually...";
            } else {
                searchInput.style.display = 'none';
            }

            // Update button text
            const buttonTexts = {
                manual: 'Start Manual Audit',
                rfid: 'Start RFID Scanning',
                barcode: 'Start Barcode Scanning'
            };
            document.getElementById('startScanning').textContent = buttonTexts[method];
        }
        
        function updateScannedAssetsTable() {
            const scannedTableBody = document.getElementById('scannedAssetsTableBody');
            scannedTableBody.innerHTML = '';
            
            scannedAssets.forEach(asset => {
                const row = document.createElement('tr');
                
                // Description
                const descCell = document.createElement('td');
                descCell.textContent = asset.description;
                row.appendChild(descCell);
                
                // Asset ID
                const idCell = document.createElement('td');
                idCell.textContent = asset.id;
                row.appendChild(idCell);
                
                // Brand/Model
                const brandModelCell = document.createElement('td');
                brandModelCell.textContent = `${asset.brand} ${asset.model}`;
                row.appendChild(brandModelCell);
                
                // Location
                const locationCell = document.createElement('td');
                locationCell.textContent = asset.room_id; // Would need room name instead of ID
                row.appendChild(locationCell);
                
                // Status
                const statusCell = document.createElement('td');
                const statusIndicator = document.createElement('span');
                statusIndicator.className = `status-dot status-${asset.status === 'present' ? 'good' : 'poor'}`;
                statusCell.appendChild(statusIndicator);
                statusCell.appendChild(document.createTextNode(' ' + asset.status));
                row.appendChild(statusCell);
                
                // Assignee
                const assigneeCell = document.createElement('td');
                assigneeCell.textContent = asset.assignee_id; // Need to display assignee name
                row.appendChild(assigneeCell);
                
                // Last Updated
                const lastUpdatedCell = document.createElement('td');
                const date = new Date(asset.last_update);
                lastUpdatedCell.textContent = date.toLocaleDateString();
                row.appendChild(lastUpdatedCell);
                
                scannedTableBody.appendChild(row);
            });
        }
        
        //AYOOO
        // Updated implementation without simulateScanAsset()

        // Global variables for scanner functionality
        let isScanning = false;
        let scanBuffer = '';
        let scanTimeout = null;
        const SCAN_TIMEOUT_MS = 20; // Timeout between scanner inputs

        function startBarcodeScan() {
            if (currentAuditMethod !== 'barcode') return;
            
            isScanning = true;
            scanBuffer = '';
            document.getElementById('startScanning').textContent = 'Scanning... (Click to Stop)';
            document.getElementById('startScanning').classList.remove('btn-primary');
            document.getElementById('startScanning').classList.add('btn-danger');
            
            // Show a scanning indicator
            const searchContainer = document.getElementById('searchContainer');
            let scanIndicator = document.getElementById('scanIndicator');
            
            if (!scanIndicator) {
                scanIndicator = document.createElement('div');
                scanIndicator.id = 'scanIndicator';
                scanIndicator.className = 'alert alert-info mt-2';
                scanIndicator.innerHTML = '<strong>Barcode scanning active</strong><br>Scan assets or click the button above to stop scanning';
                searchContainer.appendChild(scanIndicator);
            } else {
                scanIndicator.style.display = 'block';
            }
            
            // Add event listener for barcode scanner input
            document.addEventListener('keypress', handleScannerInput);
        }

        function stopBarcodeScan() {
            if (!isScanning) return;
            
            isScanning = false;
            document.getElementById('startScanning').textContent = 'Start Barcode Scanning';
            document.getElementById('startScanning').classList.remove('btn-danger');
            document.getElementById('startScanning').classList.add('btn-primary');
            
            // Hide scanning indicator
            const scanIndicator = document.getElementById('scanIndicator');
            if (scanIndicator) {
                scanIndicator.style.display = 'none';
            }
            
            // Remove event listener
            document.removeEventListener('keypress', handleScannerInput);
        }

        function handleScannerInput(e) {
            // If we're in an input field, don't process as scanner input
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }
            
            // Clear existing timeout and set a new one
            if (scanTimeout) {
                clearTimeout(scanTimeout);
            }
            
            // If Enter key is pressed, process the accumulated buffer
            if (e.key === 'Enter') {
                processScanBuffer();
                return;
            }
            
            // Add character to buffer
            scanBuffer += e.key;
            
            // Set timeout to process buffer if no more input is received
            scanTimeout = setTimeout(() => {
                if (scanBuffer.length > 0) {
                    processScanBuffer();
                }
            }, SCAN_TIMEOUT_MS);
            
            // Prevent default to avoid triggering other keyboard shortcuts
            e.preventDefault();
        }

        function processScanBuffer() {
            if (scanBuffer.length === 0) return;
            
            console.log('Scanned barcode:', scanBuffer);
            
            // Find the asset with this ID or barcode
            const asset = expectedAssets.find(a => 
                a.id === scanBuffer || 
                (a.barcode && a.barcode === scanBuffer)
            );
            
            if (asset) {
                // Asset found in expected list - mark as found
                markAssetAsFound(asset);
                
                // Show success message
                showScanMessage(`Asset found: ${asset.description} (${asset.id})`, 'success');
            } else {
                // Asset not in expected list
                showScanMessage(`Unknown asset: ${scanBuffer}`, 'warning');
                
                // Optionally, add this as an unexpected asset
                addUnexpectedAsset(scanBuffer);
            }
            
            // Clear the buffer
            scanBuffer = '';
        }

        function markAssetAsFound(asset) {
            // Mark the asset as found
            asset.found = true;
            
            // Update the found status in the table
            const foundCell = document.getElementById(`found-status-${asset.id}`);
            if (foundCell) {
                foundCell.className = 'found-yes';
                foundCell.textContent = 'YES';
            }
            
            // Add to scanned assets if not already there
            if (!scannedAssets.find(a => a.id === asset.id)) {
                scannedAssets.push(asset);
                updateScannedAssetsTable();
            }
            
            // Update scan counter
            updateScanCounter();
        }

        function updateScanCounter() {
            // Count how many assets have been found
            const foundCount = expectedAssets.filter(asset => asset.found).length;
            const totalCount = expectedAssets.length;
            
            // Update or create counter element
            let scanCounter = document.getElementById('scanCounter');
            if (!scanCounter) {
                scanCounter = document.createElement('div');
                scanCounter.id = 'scanCounter';
                scanCounter.className = 'alert alert-primary mt-3';
                document.getElementById('assetList').insertBefore(scanCounter, document.getElementById('assetList').firstChild);
            }
            
            // Update counter text
            scanCounter.innerHTML = `<strong>Asset Scan Progress:</strong> ${foundCount} of ${totalCount} assets found (${Math.round(foundCount/totalCount*100)}%)`;
            
            // If all assets found, show completion message
            if (foundCount === totalCount) {
                scanCounter.className = 'alert alert-success mt-3';
                scanCounter.innerHTML += '<br><strong>✓ All assets accounted for!</strong>';
            }
        }

        function showScanMessage(message, type) {
            // Create or update scan message element
            let scanMessage = document.getElementById('scanMessage');
            
            if (!scanMessage) {
                scanMessage = document.createElement('div');
                scanMessage.id = 'scanMessage';
                document.getElementById('searchContainer').appendChild(scanMessage);
            } else {
                // Clear any existing timeout
                if (scanMessage.hideTimeout) {
                    clearTimeout(scanMessage.hideTimeout);
                }
            }
            
            // Set message content and styling
            scanMessage.className = `alert alert-${type} mt-2`;
            scanMessage.textContent = message;
            scanMessage.style.display = 'block';
            
            // Auto-hide after a few seconds
            scanMessage.hideTimeout = setTimeout(() => {
                scanMessage.style.display = 'none';
            }, 3000);
        }

        // Function to handle unexpected assets
        function addUnexpectedAsset(barcode) {
            // Create an unexpected asset object
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
            
            // Add to scanned assets list
            scannedAssets.push(unexpectedAsset);
            updateScannedAssetsTable();
            
            // Optionally, you could also add to a separate "unexpected assets" list
            // that could be reported for inventory reconciliation
        }

        function updateScannedAssetsTable() {
            const scannedTableBody = document.getElementById('scannedAssetsTableBody');
            scannedTableBody.innerHTML = '';
            
            // Sort scanned assets with most recent first
            const sortedAssets = [...scannedAssets].sort((a, b) => {
                // If one is unexpected and one isn't, show unexpected first
                if (a.status === 'unexpected' && b.status !== 'unexpected') return -1;
                if (a.status !== 'unexpected' && b.status === 'unexpected') return 1;
                
                // Otherwise sort by scan time (most recent first)
                return new Date(b.last_update) - new Date(a.last_update);
            });
            
            sortedAssets.forEach(asset => {
                const row = document.createElement('tr');
                
                // Add a highlight class for unexpected assets
                if (asset.status === 'unexpected') {
                    row.className = 'table-warning';
                }
                
                // Description
                const descCell = document.createElement('td');
                descCell.textContent = asset.description;
                row.appendChild(descCell);
                
                // Asset ID
                const idCell = document.createElement('td');
                idCell.textContent = asset.id;
                row.appendChild(idCell);
                
                // Brand/Model
                const brandModelCell = document.createElement('td');
                brandModelCell.textContent = `${asset.brand} ${asset.model}`;
                row.appendChild(brandModelCell);
                
                // Location
                const locationCell = document.createElement('td');
                // Try to get the room name if available
                const roomSelect = document.getElementById('roomSelect');
                const roomName = roomSelect ? 
                    roomSelect.options[roomSelect.selectedIndex].textContent : 
                    `Room ${asset.room_id}`;
                locationCell.textContent = roomName;
                row.appendChild(locationCell);
                
                // Status
                const statusCell = document.createElement('td');
                const statusIndicator = document.createElement('span');
                
                if (asset.status === 'unexpected') {
                    statusIndicator.className = 'status-dot status-warning';
                    statusCell.appendChild(statusIndicator);
                    statusCell.appendChild(document.createTextNode(' Unexpected'));
                } else if (asset.status === 'present') {
                    statusIndicator.className = 'status-dot status-good';
                    statusCell.appendChild(statusIndicator);
                    statusCell.appendChild(document.createTextNode(' Present'));
                } else {
                    statusIndicator.className = 'status-dot status-poor';
                    statusCell.appendChild(statusIndicator);
                    statusCell.appendChild(document.createTextNode(' ' + asset.status));
                }
                row.appendChild(statusCell);
                
                // Assignee
                const assigneeCell = document.createElement('td');
                assigneeCell.textContent = asset.assignee_id; // Need to display assignee name
                row.appendChild(assigneeCell);
                
                // Last Updated
                const lastUpdatedCell = document.createElement('td');
                // For scanned items, show the time too, not just the date
                const date = new Date(asset.last_update);
                lastUpdatedCell.textContent = date.toLocaleString();
                row.appendChild(lastUpdatedCell);
                
                scannedTableBody.appendChild(row);
            });
            
            // Show the scanned assets list if we have items
            if (scannedAssets.length > 0) {
                document.getElementById('scannedAssetsList').style.display = 'block';
            }
        }

        // Update the existing setAuditMethod function to handle scanning mode changes
        function setAuditMethod(method) {
            // Stop any active scanning when changing methods
            if (isScanning) {
                stopBarcodeScan();
            }
            
            currentAuditMethod = method;
            
            document.querySelectorAll('.audit-method-btn').forEach(btn => {
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-light');
            });

            const activeBtn = document.querySelector(`.audit-method-btn[onclick="setAuditMethod('${method}')"]`);
            activeBtn.classList.remove('btn-light');
            activeBtn.classList.add('btn-primary');

            // Show search bar only for manual mode
            const searchInput = document.getElementById('searchInput');
            if (method === 'manual') {
                searchInput.style.display = 'block';
                searchInput.placeholder = "Search assets manually...";
            } else {
                searchInput.style.display = 'none';
            }

            // Update button text
            const buttonTexts = {
                manual: 'Start Manual Audit',
                rfid: 'Start RFID Scanning',
                barcode: 'Start Barcode Scanning'
            };
            document.getElementById('startScanning').textContent = buttonTexts[method];
        }

        // Manual asset search function
        async function manualSearchAsset() {
            const searchInput = document.getElementById('searchInput');
            const assetId = searchInput.value.trim();
           
            if (!assetId) {
                showScanMessage('Please enter an asset ID', 'warning');
                return;
            }
        
            try {
                // Fetch asset details from the backend
                const response = await fetch(`/api/asset/${assetId}`);
                
                if (!response.ok) {
                    // If asset not found in the backend
                    showScanMessage(`Asset not found: ${assetId}`, 'warning');
                    
                    // Option to add as unexpected
                    if (confirm(`Asset "${assetId}" not found in system. Add as unexpected?`)) {
                        addUnexpectedAsset(assetId);
                    }
                    return;
                }
        
                // Parse the asset details
                const asset = await response.json();
        
                // Mark the asset as found
                markAssetAsFound(asset);
                showScanMessage(`Asset found: ${asset.description} (${asset.id})`, 'success');
        
            } catch (error) {
                console.error('Error searching for asset:', error);
                showScanMessage('An error occurred while searching for the asset', 'error');
            }
        }

        // Update the click handler for the scanning button
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('startScanning').addEventListener('click', function() {
                if (currentAuditMethod === 'barcode') {
                    if (!isScanning) {
                        const buildingName = document.querySelector(`#buildingSelect option[value="${currentBuilding}"]`).textContent;
                        const floorName = document.querySelector(`#floorSelect option[value="${currentFloor}"]`).textContent;
                        const roomName = document.querySelector(`#roomSelect option[value="${currentRoom}"]`).textContent;
                        
                        console.log(`Started ${currentAuditMethod} audit for ${buildingName}, ${floorName}, ${roomName}`);
                        startBarcodeScan();
                    } else {
                        stopBarcodeScan();
                    }
                } else if (currentAuditMethod === 'manual') {
                    // For manual mode, focus on the input
                    document.getElementById('searchInput').focus();
                } else if (currentAuditMethod === 'rfid') {
                    // Placeholder for RFID implementation
                    alert('RFID scanning functionality not yet implemented');
                }
            });
            
            // Set up event listener for manual search
            document.getElementById('searchInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    manualSearchAsset();
                }
            });
        });