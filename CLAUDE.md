# CLAUDE.md - AI Assistant Guide for Ganyupian Repository

## Project Overview

**Project Name**: Ganyupian (甘雨片) - Stock Index Futures Basis Monitoring System
**Purpose**: Real-time monitoring and analysis of Chinese stock index futures basis spreads
**Language**: Primarily Chinese (中文)
**Type**: Financial monitoring tool with both web and Python implementations

This repository contains tools for monitoring the basis (price difference between spot and futures) for Chinese stock index futures traded on China Financial Futures Exchange (CFFEX):
- **IF** - CSI 300 Index Futures (沪深300股指期货)
- **IH** - SSE 50 Index Futures (上证50股指期货)
- **IC** - CSI 500 Index Futures (中证500股指期货)
- **IM** - CSI 1000 Index Futures (中证1000股指期货)

---

## Repository Structure

```
ganyupian/
├── index.html                          # Project portal/index page
├── 期货监控/                           # Futures monitoring (static web version)
│   └── index.html                      # Main monitoring dashboard
├── 期货监控PY/                         # Futures monitoring (Python version)
│   ├── jiankong.py                     # Streamlit application
│   └── requirements.txt                # Python dependencies
└── f449d1cdb4eb4b83b24337d18f0ce8aa.txt  # Git reference hash
```

### File Descriptions

#### `/index.html`
- **Purpose**: Landing page that serves as a project portal
- **Content**: Links to static web app and downloadable Python files
- **Target**: GitHub Pages deployment
- **Note**: Explains that Python files cannot run on GitHub Pages and provides download links

#### `/期货监控/index.html`
- **Purpose**: Full-featured static web application for futures monitoring
- **Size**: ~900 lines of self-contained HTML/CSS/JavaScript
- **Key Features**:
  - Real-time data fetching from Sina Finance and East Money APIs
  - Multi-contract switching (IF/IH/IC/IM)
  - Basis calculations with annualization
  - Market hours detection
  - LocalStorage caching for offline viewing
  - Responsive mobile-first design
  - Fallback data when APIs are unavailable
- **Data Sources**:
  - Primary: Sina Finance (`http://hq.sinajs.cn/list=`)
  - Fallback: East Money (`https://push2.eastmoney.com/api/qt/ulist.np/get`)
- **Trading Hours Detection**: 9:30-11:30, 13:00-15:00 on weekdays

#### `/期货监控PY/jiankong.py`
- **Purpose**: Python/Streamlit version of the monitoring tool
- **Framework**: Streamlit
- **Data Source**: AkShare library
- **Features**:
  - Manual refresh button
  - Real-time spot and futures price fetching
  - Basis calculation with percentage display
  - DataFrame visualization

#### `/期货监控PY/requirements.txt`
- **Dependencies**:
  - `streamlit` - Web framework
  - `akshare` - Financial data API
  - `pandas` - Data manipulation

---

## Key Technical Concepts

### 1. Basis (基差)
**Formula**: `Basis = Spot Price - Futures Price`

- **Positive Basis**: Futures trading below spot (backwardation/贴水)
- **Negative Basis**: Futures trading above spot (contango/升水)

### 2. Annualized Basis (年化基差)
**Formula**: `Annual Basis % = (Basis / Spot Price) × (365 / Days Left) × 100`

Represents the annualized return if holding until contract expiration.

### 3. Contract Months
Standard format: `YYMM` (e.g., `2601` = January 2026)
- Expires on the 3rd Friday of the expiration month
- Current monitoring: 2601, 2602, 2603, 2606

### 4. Daily Discount (日平均折价)
**Formula**: `Daily Discount = Basis / Days Left`

Average daily price convergence rate.

### 5. Annualized Point Discount (年化每点折)
**Formula**: `Annual Point Discount = (Daily Discount × 365) / 10`

Helps traders assess arbitrage opportunities.

---

## Development Workflows

### Working with the Static Web App (`期货监控/index.html`)

#### Testing Locally
1. Simply open the HTML file in a browser
2. No build process or server required
3. Note: CORS restrictions may apply to API calls in local file:// protocol

#### Deploying to GitHub Pages
1. Ensure the file is in the repository root or appropriate directory
2. Enable GitHub Pages in repository settings
3. The static HTML works without any build step
4. Landing page (`/index.html`) provides navigation

#### Key Code Sections

**Line 318-372**: Global configuration object
```javascript
const CONFIG = {
    contractConfig: { IF, IH, IC, IM configs with fallback data },
    currentContract: 'IF',
    contracts: ['2601', '2602', '2603', '2606'],
    refreshInterval: 2000,
    ...
}
```

**Line 374-399**: LocalStorage utilities for caching
- `saveToLocalStorage(contract, data)` at line 376
- `getFromLocalStorage(contract)` at line 389

**Line 447-468**: Market hours detection
- `checkMarketStatus()` at line 448
- Weekday detection at line 455
- Trading hours: 9:30-11:30, 13:00-15:00

**Line 471-559**: Sina Finance data fetching
- `fetchSinaData()` at line 472
- JSONP-style dynamic script injection
- Timeout handling (1500ms default)
- Automatic caching on successful fetch

**Line 561-647**: East Money fallback data source
- `fetchEastMoneyData()` at line 562
- Used when Sina fails
- Similar caching mechanism

**Line 649-676**: Main data fetching orchestrator
- `fetchData()` at line 650
- Source switching logic
- Cascading fallback: Sina → East Money → LocalStorage → Hardcoded fallback

**Line 678-716**: Indicator calculations
- `calculateIndicators(rawData)` at line 680
- Implements all financial formulas
- Tracks basis changes over time

**Line 718-754**: UI update logic
- `updateTable(calcData)` at line 719
- DOM manipulation for data display
- Rise/fall color coding

**Line 756-790**: Contract switching
- `switchContract(contractCode)` at line 757
- Tab interface with keyboard support

**Line 840-859**: Auto-refresh timer
- Default: 2000ms (2 seconds)
- Fast mode: 1000ms (1 second)

### Working with Python Version (`期货监控PY/jiankong.py`)

#### Running Locally
```bash
cd 期货监控PY
pip install -r requirements.txt
streamlit run jiankong.py
```

#### Key Code Sections

**Line 7**: Streamlit page config
**Line 11-12**: Manual refresh button with `st.rerun()`
**Line 20**: AkShare spot data fetching
**Line 23-28**: Target index definitions
**Line 32-52**: Data processing loop
- Spot price lookup at line 34
- Futures data from AkShare at line 39
- Basis calculations at line 43-44

#### Deployment
- Can be deployed to Streamlit Cloud
- Requires public repository or Streamlit sharing
- Note: API access from deployment environment may vary

---

## AI Assistant Guidelines

### 1. Language Considerations
- **Primary Language**: Chinese (Simplified)
- **Code Comments**: Mix of Chinese and English
- **User Interface**: All Chinese
- **Financial Terms**: Use Chinese terminology when adding features
- When providing explanations, adapt to user's language preference

### 2. Financial Domain Knowledge
- Understand basis trading and arbitrage concepts
- Respect market hours (9:30-11:30, 13:00-15:00 China Standard Time)
- Be aware of contract expiration rules (3rd Friday)
- Handle market holidays appropriately

### 3. Code Modification Best Practices

#### For Static HTML (`期货监控/index.html`)
- **Self-contained**: Keep all code in single HTML file
- **Mobile-first**: Test responsive design changes
- **Fallback data**: Always maintain fallback data for contracts
- **Error handling**: Network failures are common, always provide graceful degradation
- **LocalStorage**: Persist data for offline viewing
- **CORS-friendly**: Use JSONP or appropriate cross-origin techniques
- **No external dependencies**: Avoid adding npm packages or build steps

#### For Python Version (`期货监控PY/jiankong.py`)
- **Dependencies**: Minimize new dependencies
- **AkShare compatibility**: Check AkShare documentation for API changes
- **Streamlit best practices**: Use caching, session state appropriately
- **Error messages**: Chinese error messages for end users

### 4. Data Source Reliability
- **Sina Finance**: Primary but may be rate-limited or blocked
- **East Money**: Good fallback option
- **AkShare**: Python library wrapping multiple sources
- **Always implement**: Timeout handling, retry logic, fallback mechanisms
- **Never assume**: API availability or format stability

### 5. Testing Checklist
Before proposing changes, verify:
- [ ] Handles closed market hours gracefully
- [ ] Works with missing API data (uses fallback)
- [ ] Mobile responsive (especially for HTML version)
- [ ] LocalStorage quota limits respected
- [ ] Calculations are mathematically correct
- [ ] Timezone handling (China Standard Time, UTC+8)
- [ ] Weekend/holiday detection

### 6. Common Modification Scenarios

#### Adding a New Contract Month
1. Update `CONFIG.contracts` array (line 364 in HTML)
2. Add table headers in HTML template (line 265)
3. Add row cells with correct IDs
4. Ensure fallback data includes new month
5. Update expiration date calculation if needed

#### Adding a New Index (e.g., IG for Growth Enterprise)
1. Add to `CONFIG.contractConfig` (line 321)
2. Include spot price source
3. Provide complete fallback data set
4. Add tab to contract-tabs div (line 243)
5. Update Python version targets array (line 23)

#### Modifying Refresh Interval
- Default: `CONFIG.refreshInterval = 2000` (line 365)
- Fast mode: 1000ms (line 812)
- Consider API rate limits before decreasing

#### Adding New Indicators
1. Add calculation in `calculateIndicators()` (line 680)
2. Add table row in HTML structure (line 272-281)
3. Update `updateTable()` to display new indicator (line 719)
4. Document the formula in this file

### 7. Security Considerations
- **XSS Prevention**: All user inputs should be sanitized
- **CORS**: Only use trusted API endpoints
- **LocalStorage**: Don't store sensitive data
- **API Keys**: None currently required, maintain this if possible
- **HTTPS**: Prefer HTTPS endpoints (note: Sina uses HTTP)

### 8. Performance Optimization
- **Caching**: LocalStorage caching is implemented
- **Debouncing**: Consider for rapid user interactions
- **DOM Updates**: Batch updates when possible
- **API Calls**: Respect rate limits, use timeout values
- **Mobile**: Minimize reflows, optimize CSS selectors

### 9. Debugging Tips
- **Browser Console**: Check for CORS, network errors
- **Network Tab**: Monitor API response times and failures
- **LocalStorage Inspector**: Verify cached data structure
- **Market Hours**: Many issues occur outside trading hours
- **Data Validation**: Always log API response structure changes

### 10. Git Workflow
- **Branch naming**: Use `claude/` prefix for AI-generated branches
- **Commit messages**: Chinese or English, be descriptive
- **Current branch**: `claude/claude-md-mkruiff2nxpgz776-mTO73`
- **Main branch**: (not specified, likely `main` or `master`)
- **Push command**: `git push -u origin <branch-name>`

---

## Common Issues and Solutions

### Issue: APIs not returning data
**Solution**: Check fallback chain - Sina → East Money → LocalStorage → Hardcoded fallback

### Issue: Incorrect basis calculations
**Solution**: Verify spot price source matches futures contract underlying index

### Issue: Mobile display issues
**Solution**: Test with viewport meta tag, check CSS media queries (line 223)

### Issue: Streamlit app slow
**Solution**: Add `@st.cache_data` decorators, reduce API call frequency

### Issue: Contract expiration date wrong
**Solution**: Review `calculateDaysLeft()` function (line 415), verify 3rd Friday logic

---

## Future Enhancement Ideas

1. **Historical Data**: Store and display historical basis trends
2. **Alerts**: Browser notifications for basis threshold triggers
3. **Comparison View**: Side-by-side contract comparison
4. **Export**: CSV/Excel export functionality
5. **Charts**: Visual basis trend lines using Chart.js or similar
6. **Backend**: Optional Python FastAPI backend for data aggregation
7. **Database**: Store historical data in SQLite or PostgreSQL
8. **Authentication**: Multi-user support with portfolios
9. **Real-time WebSocket**: Replace polling with WebSocket for live data
10. **Advanced Indicators**: Volatility, volume-weighted basis, etc.

---

## Glossary (Chinese ↔ English)

| Chinese | English | Notes |
|---------|---------|-------|
| 基差 | Basis | Spot - Futures price |
| 年化基差 | Annualized Basis | Annualized return % |
| 贴水 | Backwardation | Futures < Spot |
| 升水 | Contango | Futures > Spot |
| 未平仓量 | Open Interest | Contracts not yet closed |
| 成交量 | Volume | Contracts traded |
| 日平均折价 | Daily Discount | Basis per day |
| 年化每点折 | Annual Point Discount | Trading cost metric |
| 主力合约 | Main Contract | Most liquid contract |
| 现货 | Spot | Cash/index price |
| 期货 | Futures | Derivative contract |

---

## Version History

- **Initial Version**: Static HTML futures monitoring dashboard
- **Python Addition**: Streamlit-based alternative implementation
- **Cache Enhancement**: LocalStorage support for offline viewing
- **Multi-source**: Sina + East Money dual API support

---

## Contact and Contribution

For questions or contributions:
1. Check existing code comments (many in Chinese)
2. Test thoroughly before submitting
3. Maintain backward compatibility
4. Document changes in commit messages

---

## Quick Reference Commands

```bash
# View repository status
git status

# Create new feature branch
git checkout -b claude/<session-id>-<feature>

# Run Python version locally
cd 期货监控PY && streamlit run jiankong.py

# Commit changes
git add .
git commit -m "Description of changes"

# Push to remote (with retry logic for network issues)
git push -u origin <branch-name>
```

---

**Last Updated**: 2026-01-24
**Document Version**: 1.0
**Maintained by**: AI Assistants working with this codebase
