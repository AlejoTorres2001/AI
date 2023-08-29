import { PDFDownloadLink } from '@react-pdf/renderer'
import PDFDocument from './PDFDocument'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFilePdf,faArrowDown} from '@fortawesome/free-solid-svg-icons';
import "../styles/PDFDownload.css"

function PDFDownload({summary, selectedFileName}:{summary:string, selectedFileName:string}) {
  return (
    <>
    <PDFDownloadLink document={<PDFDocument text={summary} />} fileName={`${selectedFileName}_summary.pdf`}>
      {({ blob, url, loading, error }) => (<button disabled={loading} className='download-button'>
        <FontAwesomeIcon icon={faFilePdf} className='icon' />
        <FontAwesomeIcon icon={faArrowDown} className='icon' />
      </button>)}
    </PDFDownloadLink>
    </>
  )
}

export default PDFDownload