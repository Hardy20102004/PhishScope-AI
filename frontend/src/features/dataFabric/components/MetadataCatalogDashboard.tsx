import React, { useState, useEffect } from 'react';
import { dataFabricApi } from '../api/dataFabricApi';
import { MetadataNode } from '../types';

const MetadataCatalogDashboard: React.FC = () => {
  const [nodes, setNodes] = useState<MetadataNode[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchNodes = async () => {
      try {
        const data = await dataFabricApi.getMetadataNodes();
        setNodes(data);
      } catch (error) {
        console.error('Failed to fetch metadata nodes', error);
      } finally {
        setLoading(false);
      }
    };
    fetchNodes();
  }, []);

  if (loading) {
    return <div className="p-6">Loading Metadata Catalog...</div>;
  }

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Metadata Catalog</h2>
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {nodes.map((node) => (
            <li key={node.id} className="p-4 hover:bg-gray-50">
              <div className="flex justify-between">
                <div>
                  <h3 className="text-lg font-medium text-blue-600">{node.name}</h3>
                  <p className="text-sm text-gray-500">{node.description}</p>
                </div>
                <div className="text-sm text-gray-500">
                  <span className="px-2 py-1 bg-gray-100 rounded text-xs font-semibold mr-2">{node.type}</span>
                  {node.classification_label && (
                    <span className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs font-semibold">{node.classification_label}</span>
                  )}
                </div>
              </div>
            </li>
          ))}
          {nodes.length === 0 && (
            <li className="p-4 text-center text-gray-500">No metadata nodes found.</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default MetadataCatalogDashboard;
