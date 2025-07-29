import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { FileText, Calendar, Download, Eye } from 'lucide-react'
import { reportApi } from '../services/api'

interface Report {
  id: number
  title: string
  description?: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  created_at: string
  updated_at: string
  file_url?: string
}

const Reports = () => {
  const [statusFilter, setStatusFilter] = useState<string>('all')

  const { data: reports, isLoading, error } = useQuery({
    queryKey: ['reports'],
    queryFn: () => reportApi.getReports(),
  })

  const filteredReports = reports?.data?.filter((report: Report) =>
    statusFilter === 'all' || report.status === statusFilter
  ) || []

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'processing':
        return 'bg-blue-100 text-blue-800'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
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
        Error loading reports. Please try again.
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
          <p className="mt-2 text-gray-600">
            View and manage generated reports
          </p>
        </div>
        <button className="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500">
          <FileText className="mr-2 h-4 w-4" />
          Generate Report
        </button>
      </div>

      {/* Filter */}
      <div className="mb-6">
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="block rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-blue-600 sm:text-sm sm:leading-6"
        >
          <option value="all">All Reports</option>
          <option value="pending">Pending</option>
          <option value="processing">Processing</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
        </select>
      </div>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {filteredReports.map((report: Report) => (
          <div
            key={report.id}
            className="overflow-hidden rounded-lg bg-white shadow hover:shadow-md transition-shadow"
          >
            <div className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <FileText className="h-8 w-8 text-blue-500" />
                  <div className="ml-3">
                    <h3 className="text-lg font-medium text-gray-900">
                      {report.title}
                    </h3>
                  </div>
                </div>
                <span
                  className={`inline-flex rounded-full px-2 py-1 text-xs font-semibold ${getStatusColor(
                    report.status
                  )}`}
                >
                  {report.status.charAt(0).toUpperCase() + report.status.slice(1)}
                </span>
              </div>

              {report.description && (
                <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                  {report.description}
                </p>
              )}

              <div className="mt-4 flex items-center text-sm text-gray-500">
                <Calendar className="mr-1 h-4 w-4" />
                Created: {new Date(report.created_at).toLocaleDateString()}
              </div>

              <div className="mt-4 flex items-center justify-between">
                <div className="flex space-x-2">
                  <button className="inline-flex items-center rounded-md bg-gray-100 px-2 py-1 text-xs font-medium text-gray-700 hover:bg-gray-200">
                    <Eye className="mr-1 h-3 w-3" />
                    View
                  </button>
                  {report.status === 'completed' && report.file_url && (
                    <button className="inline-flex items-center rounded-md bg-blue-100 px-2 py-1 text-xs font-medium text-blue-700 hover:bg-blue-200">
                      <Download className="mr-1 h-3 w-3" />
                      Download
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredReports.length === 0 && (
        <div className="text-center py-12">
          <FileText className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No reports</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by generating your first report.
          </p>
        </div>
      )}
    </div>
  )
}

export default Reports
