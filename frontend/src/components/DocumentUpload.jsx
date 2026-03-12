import { useState } from 'react'

export default function DocumentUpload() {
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')

  const handleUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setUploading(true)
    setMessage('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      setMessage(`✓ ${data.filename} uploaded and indexed`)
    } catch (error) {
      setMessage('✗ Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="document-upload">
      <label className="upload-btn">
        {uploading ? 'Uploading...' : '📄 Upload Document'}
        <input type="file" onChange={handleUpload} accept=".pdf,.md" disabled={uploading} />
      </label>
      {message && <span className="upload-message">{message}</span>}
    </div>
  )
}
