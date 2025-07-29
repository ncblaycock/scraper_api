import { useQuery } from '@tanstack/react-query'
import { Download, File, Calendar, FileText } from 'lucide-react'
import { downloadApi } from '../services/api'

interface DownloadItem {
  id: number
  filename: string
  file_type: string
  file_size: number
  created_at: string
  download_count: number
  url: string
}

const Downloads = () => {
  const { data: downloads, isLoading, error } = useQuery({
    queryKey: ['downloads'],
    queryFn: () => downloadApi.getDownloads(),
  })

  const handleDownload = async (downloadItem: DownloadItem) => {
    try {
      const response = await downloadApi.downloadFile(downloadItem.id)
      const blob = new Blob([response.data])
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = downloadItem.filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (fileType: string) => {
    if (fileType.includes('pdf')) return <FileText className="h-8 w-8 text-red-500" />
    if (fileType.includes('excel') || fileType.includes('csv')) return <File className="h-8 w-8 text-green-500" />
    return <File className="h-8 w-8 text-gray-500" />
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center text-red-600">
        Error loading downloads. Please try again.
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Downloads</h1>
        <p className="mt-2 text-gray-600">
          Access and download available files
        </p>
      </div>

      {/* Downloads List */}
      <div className="overflow-hidden rounded-lg bg-white shadow">
        <ul className="divide-y divide-gray-200">
          {downloads?.data?.map((item: DownloadItem) => (
            <li key={item.id} className="px-6 py-4 hover:bg-gray-50">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    {getFileIcon(item.file_type)}
                  </div>
                  <div className="ml-4">
                    <div className="text-sm font-medium text-gray-900">
                      {item.filename}
                    </div>
                    <div className="text-sm text-gray-500">
                      {item.file_type} • {formatFileSize(item.file_size)}
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <div className="flex items-center text-sm text-gray-500">
                      <Calendar className="mr-1 h-4 w-4" />
                      {new Date(item.created_at).toLocaleDateString()}
                    </div>
                    <div className="text-sm text-gray-500">
                      Downloaded {item.download_count} times
                    </div>
                  </div>
                  <button
                    onClick={() => handleDownload(item)}
                    className="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500"
                  >
                    <Download className="mr-2 h-4 w-4" />
                    Download
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>

        {(!downloads?.data || downloads.data.length === 0) && (
          <div className="text-center py-12">
            <Download className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No downloads available</h3>
            <p className="mt-1 text-sm text-gray-500">
              Files will appear here when they become available for download.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Downloads
