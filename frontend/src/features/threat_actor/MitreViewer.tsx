import React from 'react';

export const MitreViewer: React.FC<{ actorId: string }> = (_props) => {
  // Mock TTPs
  const tactics = [
    { name: 'Initial Access', techniques: ['T1566: Phishing', 'T1190: Exploit Public-Facing Application'] },
    { name: 'Execution', techniques: ['T1059: Command and Scripting Interpreter'] },
    { name: 'Persistence', techniques: ['T1543: Create or Modify System Process'] },
    { name: 'Privilege Escalation', techniques: ['T1068: Exploitation for Privilege Escalation'] },
    { name: 'Defense Evasion', techniques: ['T1140: Deobfuscate/Decode Files or Information', 'T1070: Indicator Removal'] },
    { name: 'Credential Access', techniques: ['T1003: OS Credential Dumping'] },
    { name: 'Discovery', techniques: ['T1082: System Information Discovery'] },
    { name: 'Lateral Movement', techniques: ['T1021: Remote Services'] },
    { name: 'Collection', techniques: ['T1114: Email Collection'] },
    { name: 'Exfiltration', techniques: ['T1041: Exfiltration Over C2 Channel'] },
    { name: 'Command and Control', techniques: ['T1071: Application Layer Protocol'] },
  ];

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl shadow-lg p-6 overflow-x-auto">
      <div className="flex justify-between items-center mb-6 min-w-max">
        <h3 className="text-xl font-semibold text-white flex items-center">
          <svg className="w-5 h-5 mr-2 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
          </svg>
          MITRE ATT&CK Matrix Mapping
        </h3>
        <span className="text-sm text-gray-400 bg-gray-800 px-3 py-1 rounded">Coverage: 11 Tactics, 13 Techniques</span>
      </div>

      <div className="flex space-x-4 pb-4 min-w-max">
        {tactics.map(tactic => (
          <div key={tactic.name} className="w-48 flex-shrink-0">
            <div className="bg-gray-800 text-gray-200 text-sm font-semibold p-2 mb-2 border-t-2 border-red-500 rounded-b shadow-sm">
              {tactic.name}
            </div>
            <div className="space-y-2">
              {tactic.techniques.map(tech => (
                <div key={tech} className="bg-gray-800/50 hover:bg-gray-700 border border-gray-700 text-gray-300 text-xs p-2 rounded cursor-pointer transition-colors break-words">
                  {tech}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
