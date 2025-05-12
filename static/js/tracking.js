$(document).ready(function() {
    $('#table1').DataTable({
    });

    $('#table2').DataTable({
        pageLength: 13
    });
});

function toggleTable(tableId) {
    document.getElementById('page1').classList.add('hidden');
    document.getElementById('page2').classList.add('hidden');

    document.getElementById(tableId).classList.remove('hidden');
}

function handleCellClick(matno, month) {
    const selectedYear = document.getElementById('year').value;
    const selectedCustno = document.getElementById('customer').value;
    const selectedSale = document.getElementById('salesman').value;

    const monthNames = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];

    const monthName = monthNames[month - 1];

    document.getElementById('matno').innerText = matno;
    document.getElementById('month').innerText = monthName;
    fetch('/fetch-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        matno: matno,
        month: month,
        selected_year: selectedYear,
        selected_custno: selectedCustno,
        selected_sale: selectedSale
      })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
          alert(data.error);
        } else {
          const modalPrice = document.getElementById('modal-price');
          const modalUOM = document.getElementById('modal-uom');
          const modalLastPurchase = document.getElementById('modal-last-purchase');
      
          modalPrice.innerHTML = '';
          modalUOM.innerHTML = '';
          modalLastPurchase.innerHTML = '';
      
          const prices = data.price || [];
          const uoms = data.uom || [];
          const ACTIVATGs = data.last_purchase_date || [];
      
          const headerRow = document.createElement('tr');
          headerRow.innerHTML = `
            <th>No</th>
            <th>Prices</th>
            <th>Uoms</th>
            <th>ACTIVATGs</th>
          `;
          modalPrice.appendChild(headerRow);
          modalUOM.appendChild(headerRow);
          modalLastPurchase.appendChild(headerRow);
      
          for (let i = 0; i < Math.max(prices.length, uoms.length, ACTIVATGs.length); i++) {
            const price = prices[i] || '';
            const uom = uoms[i] || '';
            let ACTIVATG = ACTIVATGs[i] || '';

            if (ACTIVATG) {
              const dateObj = new Date(ACTIVATG);
          
              if (!isNaN(dateObj.getTime())) {
                  ACTIVATG = dateObj.toLocaleDateString('en-GB', { 
                      day: '2-digit', 
                      month: '2-digit', 
                      year: 'numeric' 
                  });
              } else {
                  ACTIVATG = "-";
              }
            }
      
            const row = document.createElement('tr');
            row.innerHTML = `
              <td>${i + 1}</td>
              <td>${price}</td>
              <td>${uom}</td>
              <td>${ACTIVATG}</td>
            `;
            modalPrice.appendChild(row);
            modalUOM.appendChild(row);
            modalLastPurchase.appendChild(row);
          }
      
          document.getElementById('myModal').style.display = "block";
        }
      })
    .catch(error => console.error('Error:', error));
  }

  document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('myModal').style.display = "none";
  });

  window.onclick = function(event) {
    if (event.target == document.getElementById('myModal')) {
      document.getElementById('myModal').style.display = "none";
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    const cells = document.querySelectorAll('#table1 td');

    cells.forEach(cell => {
      cell.addEventListener('click', function() {
        const monthIndex = Array.from(cell.parentNode.children).indexOf(cell) - 5;
        if (monthIndex >= 0 && monthIndex < 12) {
          const matno = cell.closest('tr').children[1].textContent;
          handleCellClick(matno, monthIndex + 1);
        }
      });
    });
  });